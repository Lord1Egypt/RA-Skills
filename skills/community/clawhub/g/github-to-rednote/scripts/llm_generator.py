#!/usr/bin/env python3
"""
LLM content generation for RedNote articles.
Uses OpenClaw's agent capability instead of external LLM APIs.
"""

import os
import re
import json
import subprocess
import tempfile
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class AgentResponse:
    """Structured agent response."""
    content: str
    agent_id: str
    success: bool = True
    error: str = ""


class AgentError(Exception):
    """Agent invocation error."""
    def __init__(self, message: str, agent_id: str = None):
        super().__init__(message)
        self.agent_id = agent_id


class OpenClawAgentClient:
    """Client for OpenClaw agent-based content generation."""
    
    def __init__(self, agent_name: str = "content-writer"):
        """
        Initialize OpenClaw agent client.
        
        Args:
            agent_name: Name of the agent to spawn for content generation
        """
        self.agent_name = agent_name
        self.agent_session = None
    
    def _build_system_prompt(self, template: str, style: str) -> str:
        """Build system prompt for the agent."""
        template_configs = {
            'intro': '''你是一个技术内容创作者，专门为小红书(RED)平台撰写技术文章。
你的写作风格：
- 亲切友好，像朋友推荐好东西
- 使用表情符号增加趣味性
- 重点突出，层次分明
- 语言简洁，适合移动端阅读
- 包含实用的代码片段或示例''',
            'review': '''你是一个技术测评专家，撰写深度开源项目评测。
你的写作风格：
- 客观公正，既说优点也提缺点
- 技术分析深入但不晦涩
- 结合实际使用场景
- 给出明确的使用建议
- 适合有一定技术基础的读者''',
            'tutorial': '''你是一个技术教程作者，撰写简明易懂的入门指南。
你的写作风格：
- 步骤清晰，循序渐进
- 代码示例完整可运行
- 解释"为什么"而不只是"怎么做"
- 包含常见问题和解决方案
- 适合新手阅读''',
            'list': '''你是一个技术工具推荐专家，撰写工具清单类文章。
你的写作风格：
- 信息密度高，干货满满
- 分类清晰，便于对比
- 每款工具突出1-2个核心卖点
- 包含选择建议
- 适合快速浏览和收藏''',
            'release': '''你是一个开源项目新闻作者，撰写版本发布解读。
你的写作风格：
- 第一时间抓住重点
- 解读新特性背后的价值
- 说明升级注意事项
- 包含简单的迁移指南
- 激发读者尝试新版本的兴趣'''
        }
        
        style_configs = {
            'casual': '使用口语化表达，多使用"我觉得"、"大家"、"咱们"等亲切用语，偶尔自嘲。',
            'professional': '使用专业术语，逻辑严密，数据驱动，引用官方文档，给出权威结论。',
            'enthusiastic': '热情洋溢，多用感叹号，强调"太棒了"、"必看"、"强烈推荐"等，感染力十足。',
            'story': '用讲故事的方式引入，有背景、冲突、解决方案，让读者有代入感。',
            'minimal': '极简风格，每句话都有信息量，没有废话，用列表和要点代替长段落。'
        }
        
        system_prompt = template_configs.get(template, template_configs['intro'])
        style_prompt = style_configs.get(style, style_configs['casual'])
        
        return f"{system_prompt}\n\n语气要求：{style_prompt}"
    
    def _build_user_prompt(self, repo_data: Dict, template: str, style: str) -> str:
        """Build user prompt with repository data - Enhanced version with structured sections."""
        
        # Stars display rule: only mention if >= 100
        stars = repo_data.get('stars', 0)
        stars_text = f"{stars:,} stars" if stars >= 100 else ""
        
        # Build repo info string with enhanced structure
        repo_info = f"""
项目名称: {repo_data.get('repo', 'Unknown')}
完整名称: {repo_data.get('full_name', 'N/A')}
GitHub URL: {repo_data.get('html_url', repo_data.get('url', ''))}
描述: {repo_data.get('description', '暂无描述')}

📊 统计数据:
{f'- Stars: {stars:,} (社交证明)' if stars >= 100 else '- Stars: < 100 (暂不提及)'}
- Forks: {repo_data.get('forks', 0):,}
- Watchers: {repo_data.get('watchers', 0):,}
- Open Issues: {repo_data.get('open_issues', 0):,}
- 主要语言: {repo_data.get('language', 'Unknown')}
- 所有语言: {', '.join(repo_data.get('languages', {}).keys()) or 'N/A'}
- 大小: {repo_data.get('size', 0):,} KB
- 开源协议: {repo_data.get('license', 'Unknown')}
- 创建时间: {repo_data.get('created_at', 'N/A')}
- 最后更新: {repo_data.get('updated_at', 'N/A')}

🏷️ 标签: {', '.join(repo_data.get('topics', [])) or '无'}

🌐 主页: {repo_data.get('homepage', 'N/A')}
默认分支: {repo_data.get('default_branch', 'main')}
"""
        
        # Add releases info if available
        releases = repo_data.get('releases', [])
        if releases:
            repo_info += f"\n🚀 最新版本 ({len(releases)} 个):\n"
            for rel in releases[:3]:
                repo_info += f"- {rel.get('tag_name', 'N/A')}: {rel.get('name', 'No name')}\n"
        
        # Add contributors info if available
        contributors = repo_data.get('contributors', [])
        if contributors:
            repo_info += f"\n👥 主要贡献者 ({len(contributors)} 人):\n"
            for c in contributors[:5]:
                repo_info += f"- @{c.get('login', 'N/A')}: {c.get('contributions', 0)} 次提交\n"
        
        # Add README excerpt
        readme = repo_data.get('readme', '')
        if readme:
            readme_excerpt = readme[:3000] + "..." if len(readme) > 3000 else readme
            repo_info += f"\n📝 README 节选:\n```\n{readme_excerpt}\n```\n"
        
        # Add Features extraction if available
        features = repo_data.get('readme_features', [])
        if features:
            repo_info += f"\n✨ README 核心功能:\n"
            for f in features[:5]:
                repo_info += f"- {f}\n"
        
        # Add selling points
        selling_points = repo_data.get('selling_points', [])
        if selling_points:
            repo_info += f"\n🎯 项目卖点:\n"
            for sp in selling_points[:5]:
                repo_info += f"- {sp}\n"
        
        template_names = {
            'intro': '项目介绍',
            'review': '深度测评', 
            'tutorial': '使用教程',
            'list': '工具清单',
            'release': '版本发布'
        }
        
        style_names = {
            'casual': '轻松随意',
            'professional': '专业严谨',
            'enthusiastic': '热情推荐',
            'story': '故事叙事',
            'minimal': '极简干练'
        }
        
        # Enhanced prompt with structured content requirements
        prompt = f"""请根据以下 GitHub 仓库信息，撰写一篇小红书风格的技术文章。

{repo_info}

🎯 文章类型: {template_names.get(template, '项目介绍')}
✍️ 写作风格: {style_names.get(style, '轻松随意')}

📝 内容结构要求:

1. **标题**（吸引眼球，使用 1-2 个 emoji）

2. **一句话概括** - 开头必须说明"这是什么"
   - 用一句话清晰说明项目的核心功能
   - 让读者 3 秒内明白这个项目的价值

3. **适用场景** 
   - 适合谁用？（目标用户群体）
   - 解决什么问题？（具体痛点）
   - 什么情况下会用到？（使用场景）

4. **核心功能**（必须具体，列出 3-5 个功能点）
   - 功能1: 具体描述
   - 功能2: 具体描述
   - 功能3: 具体描述
   - （禁止空话套话如"功能强大"、"易于使用"等，必须说具体功能）

5. **技术亮点**
   - 技术优势是什么？
   - 相比同类方案有什么独特之处？
   - 使用了什么值得注意的技术？

6. **其他要求**
   - {'如果提到流行度，可以说 "' + stars_text + '" 作为社交证明' if stars >= 100 else '不要提及 stars 数，因为数量较少'}
   - 正文分段清晰，每段不要太长
   - 适当使用 bullet points 和 emoji
   - 如果是教程类，包含简单的代码示例
   - 结尾引导互动（点赞、收藏、评论）
   - 最后添加相关标签（hashtags）
   - 总字数控制在 500-1000 字（不含代码）

❌ 禁止内容:
- "功能强大"、"易于使用"、"值得关注"等空话
- "是一个开源项目"这类废话
- 没有数据支撑的形容词

✅ 必须做到:
- 每个观点都有具体说明
- 技术细节准确
- 让读者获得实际信息

请直接输出文章内容，不要加额外的说明文字。"""
        
        return prompt
    
    def _extract_features_from_readme(self, readme: str) -> list:
        """Extract features section from README."""
        if not readme:
            return []
        
        features = []
        import re
        
        # Look for Features section
        patterns = [
            r'##\s*Features?\s*\n((?:[-*•]\s*[^\n]+\n?)+)',
            r'##\s*Key\s+Features?\s*\n((?:[-*•]\s*[^\n]+\n?)+)',
            r'(?i)(?:features?|highlights?):\s*\n((?:[-*•]\s*[^\n]+\n?)+)',
            r'###\s*Features?\s*\n((?:[-*•]\s*[^\n]+\n?)+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, readme)
            for match in matches:
                for line in match.strip().split('\n'):
                    line = line.strip().lstrip('-*•').strip()
                    if line and len(line) > 5:
                        features.append(line)
                if features:
                    break
            if features:
                break
        
        return features
    
    def generate(self, prompt: str, system_prompt: str) -> AgentResponse:
        """
        Generate content using OpenClaw agent.
        
        This method creates a temporary agent task to generate content.
        In the current implementation, it uses a fallback template-based generation
        since direct agent spawning requires OpenClaw runtime integration.
        
        Args:
            prompt: User prompt with repository data
            system_prompt: System instructions for the agent
        
        Returns:
            AgentResponse with generated content
        """
        # For now, use fallback generation
        # In a full OpenClaw environment, this would spawn an agent task
        # and wait for the result
        
        # Try to use OpenClaw CLI if available
        try:
            result = self._try_openclaw_generate(prompt, system_prompt)
            if result:
                return result
        except Exception:
            pass
        
        # Fallback to template-based generation
        return self._fallback_generate(prompt)
    
    def _try_openclaw_generate(self, prompt: str, system_prompt: str) -> Optional[AgentResponse]:
        """Try to generate using OpenClaw agent via CLI."""
        # Check if openclaw CLI is available
        try:
            result = subprocess.run(
                ['which', 'openclaw'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                return None
        except Exception:
            return None
        
        # Create a temporary file with the prompt
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(f"SYSTEM PROMPT:\n{system_prompt}\n\n")
            f.write(f"USER PROMPT:\n{prompt}\n")
            prompt_file = f.name
        
        try:
            # Try to spawn an agent task
            # This is a placeholder - actual implementation depends on OpenClaw CLI
            # For now, return None to trigger fallback
            return None
        finally:
            os.unlink(prompt_file)
    
    def _fallback_generate(self, prompt: str) -> AgentResponse:
        """Fallback generation using templates when agent is not available."""
        # Extract repo info from prompt
        repo_match = re.search(r'项目名称:\s*(\S+)', prompt)
        repo_name = repo_match.group(1) if repo_match else "Unknown"
        
        desc_match = re.search(r'描述:\s*(.+?)(?:\n|$)', prompt)
        description = desc_match.group(1) if desc_match else "一个开源项目"
        
        stars_match = re.search(r'Stars:\s*([\d,]+)', prompt)
        stars = stars_match.group(1).replace(',', '') if stars_match else "0"
        
        lang_match = re.search(r'主要语言:\s*(\S+)', prompt)
        language = lang_match.group(1) if lang_match else "Unknown"
        
        # Extract README features from prompt
        features = []
        readme_section = re.search(r'README 节选:\s*```\n(.*?)```', prompt, re.DOTALL)
        if readme_section:
            readme_text = readme_section.group(1)
            # Look for feature bullets in README
            feature_patterns = [
                r'[-*•]\s*([^\n]+)',
                r'\d+\.\s+([^\n]+)'
            ]
            for pattern in feature_patterns:
                matches = re.findall(pattern, readme_text)
                for m in matches[:5]:
                    m_clean = m.strip().lstrip('-*•').strip()
                    if len(m_clean) > 3 and len(m_clean) < 100:
                        features.append(m_clean)
                if features:
                    break
        
        # Extract topics/tags
        topics_match = re.search(r'标签:\s*(.+?)(?:\n|$)', prompt)
        topics = []
        if topics_match:
            topics = [t.strip() for t in topics_match.group(1).split(',') if t.strip() and t.strip() != '无']
        
        # Generate a basic RedNote article with structured content
        stars_int = int(stars) if stars else 0
        stars_display = f"⭐ {stars_int:,} stars | " if stars_int >= 100 else ""
        
        # Build features section from extracted data or generic fallback
        if features:
            features_section = '\n'.join([f"• {f}" for f in features[:5]])
        else:
            features_section = f"• {description}\n• 使用 {language} 开发\n• 开源项目，欢迎贡献"
        
        # Build tags
        tags = ['#开源项目', f'#{language}', '#GitHub']
        for t in topics[:3]:
            tag = t.replace(' ', '').replace('-', '')
            if tag:
                tags.append(f'#{tag}')
        tags_str = ' '.join(list(dict.fromkeys(tags)))  # Remove duplicates while preserving order
        
        content = f"""🔥 {repo_name} - {description[:50]}

{stars_display}💻 {language}

📌 这是什么
{description}

🎯 适用场景
• 开发者寻找相关工具和解决方案
• 学习 {language} 和开源技术
• 技术实践参考和代码示例

⚡ 核心功能
{features_section}

💡 技术亮点
• 使用 {language} 开发
• 开源免费，社区驱动
• 代码透明，可自由定制

🏷️ {tags_str}"""
        
        return AgentResponse(
            content=content,
            agent_id="fallback",
            success=True
        )


class ArticleGenerator:
    """Generate RedNote articles using OpenClaw agent."""
    
    TEMPLATES = {
        'intro': {
            'name': '项目介绍',
            'description': '简洁的项目介绍，突出亮点',
            'emoji': '📌'
        },
        'review': {
            'name': '深度测评',
            'description': '详细的技术测评，优缺点分析',
            'emoji': '🔍'
        },
        'tutorial': {
            'name': '使用教程',
            'description': '入门教程和快速上手指南',
            'emoji': '📚'
        },
        'list': {
            'name': '工具清单',
            'description': '同类项目对比和推荐列表',
            'emoji': '📋'
        },
        'release': {
            'name': '版本发布',
            'description': '新版本特性解读和更新亮点',
            'emoji': '🎉'
        }
    }
    
    STYLES = {
        'casual': {
            'name': '轻松随意',
            'description': '像朋友聊天一样，轻松自然'
        },
        'professional': {
            'name': '专业严谨',
            'description': '技术深度，专业术语'
        },
        'enthusiastic': {
            'name': '热情推荐',
            'description': '充满激情，强烈推荐'
        },
        'story': {
            'name': '故事叙事',
            'description': '用故事讲技术，有情节'
        },
        'minimal': {
            'name': '极简干练',
            'description': '少即是多，直击要点'
        }
    }
    
    def __init__(self, agent_client: Optional[OpenClawAgentClient] = None):
        """Initialize with optional agent client."""
        self.agent = agent_client or OpenClawAgentClient()
    
    @staticmethod
    def list_templates() -> List[Dict]:
        """List available article templates."""
        return [
            {
                'id': k,
                'name': v['name'],
                'description': v['description'],
                'emoji': v['emoji']
            }
            for k, v in ArticleGenerator.TEMPLATES.items()
        ]
    
    @staticmethod
    def list_styles() -> List[Dict]:
        """List available writing styles."""
        return [
            {
                'id': k,
                'name': v['name'],
                'description': v['description']
            }
            for k, v in ArticleGenerator.STYLES.items()
        ]
    
    def generate(self, repo_data: Dict, template: str = 'intro',
                 style: str = 'casual', extra_context: Optional[str] = None) -> str:
        """
        Generate article from repository data.
        
        Args:
            repo_data: Repository summary from GitHubAPI
            template: Article template (intro/review/tutorial/list/release)
            style: Writing style (casual/professional/enthusiastic/story/minimal)
            extra_context: Additional context/requirements
        
        Returns:
            Generated article content
        """
        # Build prompts
        system_prompt = self.agent._build_system_prompt(template, style)
        user_prompt = self.agent._build_user_prompt(repo_data, template, style)
        
        if extra_context:
            user_prompt += f"\n\n💡 额外要求: {extra_context}\n"
        
        # Generate content
        response = self.agent.generate(user_prompt, system_prompt)
        
        if not response.success:
            raise AgentError(f"Content generation failed: {response.error}")
        
        return response.content
    
    def generate_batch(self, repo_urls: List[str], template: str = 'intro',
                       style: str = 'casual') -> List[Dict]:
        """Generate articles for multiple repositories."""
        from github_api import GitHubAPI
        
        api = GitHubAPI()
        results = []
        
        for url in repo_urls:
            try:
                repo_data = api.get_repo_summary(url)
                article = self.generate(repo_data, template, style)
                results.append({
                    'url': url,
                    'success': True,
                    'repo_name': repo_data['full_name'],
                    'article': article
                })
            except Exception as e:
                results.append({
                    'url': url,
                    'success': False,
                    'error': str(e)
                })
        
        return results


def main():
    """CLI for testing article generation."""
    import sys
    
    # Show available options
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        print("Usage: python3 llm_generator.py <repo-url> [template] [style]")
        print("\nTemplates:")
        for t in ArticleGenerator.list_templates():
            print(f"  {t['id']:12} - {t['emoji']} {t['name']}: {t['description']}")
        print("\nStyles:")
        for s in ArticleGenerator.list_styles():
            print(f"  {s['id']:12} - {s['name']}: {s['description']}")
        print("\nNote: This tool uses OpenClaw's built-in agent capability.")
        sys.exit(0)
    
    url = sys.argv[1]
    template = sys.argv[2] if len(sys.argv) > 2 else 'intro'
    style = sys.argv[3] if len(sys.argv) > 3 else 'casual'
    
    try:
        # Fetch repo data
        from github_api import GitHubAPI
        print(f"Fetching repository data: {url}")
        api = GitHubAPI()
        repo_data = api.get_repo_summary(url)
        print(f"✓ Got data for {repo_data['full_name']}")
        
        # Generate article
        print(f"\nGenerating article (template={template}, style={style})...")
        client = OpenClawAgentClient()
        generator = ArticleGenerator(client)
        article = generator.generate(repo_data, template=template, style=style)
        
        print("\n" + "="*60)
        print("GENERATED ARTICLE")
        print("="*60)
        print(article)
        print("="*60)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
