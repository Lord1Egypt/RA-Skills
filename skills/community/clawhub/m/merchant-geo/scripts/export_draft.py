#!/usr/bin/env python3
"""
多平台草稿导出工具
为没有API的平台（搜狐号、网易号、快手等）生成可直接复制粘贴的草稿格式

使用方法：
    python export_draft.py <内容文件> --platform <平台>
    python export_draft.py content.json --batch
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# 平台导出配置
PLATFORM_DRAFT_CONFIG = {
    "搜狐号": {
        "format": "html",
        "require_source": True,
        "title_prefix": "",
        "title_suffix": "",
        "special_tags": ["自媒体", "企业"]
    },
    "网易号": {
        "format": "html",
        "require_source": True,
        "title_prefix": "",
        "title_suffix": "",
        "special_tags": ["网易号", "自媒体"]
    },
    "快手": {
        "format": "video_text",
        "require_source": False,
        "title_prefix": "",
        "title_suffix": "",
        "special_tags": ["老铁", "短视频"]
    }
}


class DraftExporter:
    """草稿导出器"""
    
    def __init__(self):
        self.config = PLATFORM_DRAFT_CONFIG
    
    def load_content(self, content_path: str) -> dict:
        """加载内容文件"""
        with open(content_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def export_for_souhu(self, content: dict) -> dict:
        """
        导出搜狐号格式
        
        搜狐号特点：
        - 支持富文本编辑器
        - 必须标注来源
        - 标题长度15-30字
        """
        title = content.get("title", "")
        body = content.get("content", "")
        tags = content.get("tags", [])
        keywords = content.get("keywords", {})
        
        # 格式化正文（转换为搜狐号兼容格式）
        formatted_body = self._format_for_media(body)
        
        # 生成HTML格式
        html_content = f"""<h2>{title}</h2>

<p>来源：{content.get('enterprise_name', '原创')}</p>

{formatted_body}

<p><strong>标签：</strong>{' '.join(['#'+t for t in tags[:5]])}</p>
"""
        
        return {
            "platform": "搜狐号",
            "title": title,
            "content": html_content,
            "plain_text": f"{title}\n\n来源：{content.get('enterprise_name', '原创')}\n\n{body}",
            "tags": tags[:5],
            "source": content.get("enterprise_name", "原创"),
            "copy_ready": self._generate_copy_text(title, body, tags, source=content.get("enterprise_name")),
            "publish_guide": self._generate_souhu_guide()
        }
    
    def export_for_wangyi(self, content: dict) -> dict:
        """
        导出网易号格式
        
        网易号特点：
        - 支持HTML格式
        - 必须标注来源和作者
        - 新闻风格更受欢迎
        """
        title = content.get("title", "")
        body = content.get("content", "")
        tags = content.get("tags", [])
        
        # 格式化正文
        formatted_body = self._format_for_news(body)
        
        # 生成发布文本
        plain_text = f"""【{title}】

来源：{content.get("enterprise_name", "原创")}
作者：{content.get("legal_person", content.get("enterprise_name", "编辑"))}

{formatted_body}

# {' #'.join(tags[:5])}
"""
        
        return {
            "platform": "网易号",
            "title": title,
            "content": formatted_body,
            "plain_text": plain_text,
            "tags": tags[:3],
            "source": content.get("enterprise_name", "原创"),
            "author": content.get("legal_person", ""),
            "copy_ready": self._generate_copy_text(title, body, tags, 
                                                   source=content.get("enterprise_name"),
                                                   author=content.get("legal_person")),
            "publish_guide": self._generate_wangyi_guide()
        }
    
    def export_for_kuaishou(self, content: dict) -> dict:
        """
        导出快手格式
        
        快手特点：
        - 短视频+图文
        - 接地气风格
        - 社区互动属性
        """
        title = content.get("title", "")
        body = content.get("content", "")
        tags = content.get("tags", [])
        video_script = content.get("video_script", {})
        
        # 生成文案脚本
        if video_script:
            caption = video_script.get("hook", "")
        else:
            # 从正文中提取要点
            caption = self._extract_video_caption(body)
        
        # 快手发布文案
        kuaishou_text = f"""{caption}

{self._extract_short_body(body, 200)}

{' '.join(['#'+t if '#' in t else '#'+t for t in tags[:5]])}

老铁们，觉得有用的话点个赞呗！👍
有什么问题评论区见！
"""
        
        return {
            "platform": "快手",
            "title": title,
            "caption": caption,
            "full_text": kuaishou_text,
            "tags": tags[:3] + ["老铁#家人", "记录生活"],
            "video_script": video_script if video_script else self._generate_simple_script(body),
            "cover_suggestion": content.get("cover_suggestion", ""),
            "copy_ready": kuaishou_text,
            "publish_guide": self._generate_kuaishou_guide()
        }
    
    def _format_for_media(self, text: str) -> str:
        """格式化文本为媒体风格"""
        lines = text.split('\n')
        formatted = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 标题行
            if line.startswith('## '):
                formatted.append(f'<h3>{line[3:]}</h3>')
            elif line.startswith('### '):
                formatted.append(f'<h4>{line[4:]}</h4>')
            # 列表项
            elif line.startswith('- ') or line.startswith('* '):
                formatted.append(f'<li>{line[2:]}</li>')
            # 加粗行
            elif line.startswith('**') and line.endswith('**'):
                formatted.append(f'<strong>{line[2:-2]}</strong>')
            # 引用
            elif line.startswith('>'):
                formatted.append(f'<blockquote>{line[1:].strip()}</blockquote>')
            # 普通段落
            else:
                formatted.append(f'<p>{line}</p>')
        
        return '\n'.join(formatted)
    
    def _format_for_news(self, text: str) -> str:
        """格式化文本为新闻风格"""
        lines = text.split('\n')
        formatted = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 标题行降级
            if line.startswith('## '):
                formatted.append(f'【{line[3:]}】')
            elif line.startswith('### '):
                formatted.append(f'● {line[4:]}')
            # 列表项转换
            elif line.startswith('- ') or line.startswith('* '):
                formatted.append(f'  • {line[2:]}')
            elif line.startswith('❌'):
                formatted.append(line.replace('❌', '【误区】'))
            elif line.startswith('✅'):
                formatted.append(line.replace('✅', '【建议】'))
            # 引用保留
            elif line.startswith('>'):
                formatted.append(line)
            else:
                formatted.append(line)
        
        return '\n\n'.join(formatted)
    
    def _extract_video_caption(self, text: str) -> str:
        """从正文中提取适合视频口播的文案"""
        # 取前300字作为视频文案基础
        preview = text[:300]
        
        # 尝试提取关键句
        for line in preview.split('\n'):
            line = line.strip()
            if '！' in line or '?' in line or '？' in line:
                return line
        
        return preview.split('。')[0] if '.' in preview else preview[:100]
    
    def _extract_short_body(self, text: str, max_length: int) -> str:
        """提取短正文"""
        # 移除标题和多余格式
        lines = text.split('\n')
        content_lines = []
        
        skip_sections = ['联系方式', '关于我们', '相关阅读']
        for line in lines:
            if any(s in line for s in skip_sections):
                continue
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('*'):
                content_lines.append(line)
        
        full_text = ' '.join(content_lines)
        if len(full_text) > max_length:
            return full_text[:max_length] + '...'
        return full_text
    
    def _generate_simple_script(self, body: str) -> dict:
        """生成简单的视频脚本"""
        caption = self._extract_video_caption(body)
        
        return {
            "时长": "30-60秒",
            "开场": caption,
            "正文": self._extract_short_body(body, 300),
            "结尾": "关注我，带你了解更多干货！"
        }
    
    def _generate_copy_text(self, title: str, body: str, tags: list, 
                           source: str = None, author: str = None) -> str:
        """生成可直接复制的文本"""
        parts = []
        
        parts.append(f"【{title}】")
        parts.append("")
        
        if source or author:
            parts.append(f"来源：{source or author}")
            if author and author != source:
                parts.append(f"作者：{author}")
            parts.append("")
        
        parts.append(body)
        parts.append("")
        parts.append("标签：" + " ".join([f"#{t}" for t in tags[:5]]))
        
        return '\n'.join(parts)
    
    def _generate_souhu_guide(self) -> str:
        """生成搜狐号发布指南"""
        return """
📋 搜狐号发布指南：

1. 登录搜狐号后台 (mp.sohu.com)
2. 点击"发布文章"
3. 复制上方标题和正文内容
4. 在编辑器中粘贴（支持富文本）
5. 添加封面图（建议尺寸：900×500px）
6. 选择分类：科技/财经/房产/教育/其他
7. 添加标签：{tags}
8. 勾选"原创"标识
9. 点击"发布"

⚠️ 注意：
- 标题必须含有关键词
- 正文需保留来源标注
- 图片需有版权
"""
    
    def _generate_wangyi_guide(self) -> str:
        """生成网易号发布指南"""
        return """
📋 网易号发布指南：

1. 登录网易号后台 (mp.163.com)
2. 点击"发布内容"
3. 选择"图文"类型
4. 复制上方标题和正文内容
5. 添加封面图（建议尺寸：900×500px）
6. 选择频道分类
7. 添加摘要（50字以内）
8. 标签：{tags}
9. 点击"发布"

⚠️ 注意：
- 网易号偏好新闻资讯风格
- 必须标注来源和作者
- 时效性内容更受欢迎
"""
    
    def _generate_kuaishou_guide(self) -> str:
        """生成快手发布指南"""
        return """
📋 快手发布指南：

【图文/短视频方式】

1. 打开快手APP
2. 点击"+"发布按钮
3. 选择视频或图片素材

【图文发布】
1. 最多上传9张图片
2. 第一张作为封面
3. 复制上方文案到描述区
4. 添加话题：{tags}
5. @官方账号（如有）
6. 添加位置信息
7. 发布

【视频发布】
1. 上传视频或直接拍摄
2. 在描述区粘贴上方文案
3. 选择封面图（关键！）
4. 添加话题和位置
5. 发布

⚠️ 注意：
- 快手用户喜欢接地气内容
- 真实感比精致更重要
- 多与评论区互动
"""
    
    def export_all(self, content: dict, platforms: list = None) -> dict:
        """导出所有平台"""
        if platforms is None:
            platforms = list(PLATFORM_DRAFT_CONFIG.keys())
        
        results = {}
        
        for platform in platforms:
            if "搜狐" in platform:
                results[platform] = self.export_for_souhu(content)
            elif "网易" in platform:
                results[platform] = self.export_for_wangyi(content)
            elif "快手" in platform:
                results[platform] = self.export_for_kuaishou(content)
        
        return results
    
    def save_draft_package(self, drafts: dict, output_dir: str, enterprise_name: str):
        """保存草稿包"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 按平台保存草稿
        for platform, draft in drafts.items():
            platform_name = platform.replace("号", "").replace("快手", "kuaishou")
            draft_file = output_path / f"draft_{platform_name}.txt"
            
            with open(draft_file, 'w', encoding='utf-8') as f:
                f.write("=" * 50 + "\n")
                f.write(f"平台：{draft['platform']}\n")
                f.write("=" * 50 + "\n\n")
                f.write("【标题】\n")
                f.write(draft.get('title', '') + "\n\n")
                f.write("【正文】\n")
                f.write(draft.get('plain_text', draft.get('full_text', '')) + "\n\n")
                f.write("【标签】\n")
                f.write(', '.join(draft.get('tags', [])) + "\n\n")
                f.write("【一键复制内容】\n")
                f.write("-" * 50 + "\n")
                f.write(draft.get('copy_ready', '') + "\n")
                f.write("-" * 50 + "\n\n")
                f.write("【发布指南】\n")
                f.write(draft.get('publish_guide', '').format(tags=', '.join(draft.get('tags', []))) + "\n")
            
            print(f"✅ {platform}草稿已保存: {draft_file}")
        
        # 保存完整草稿包
        package_file = output_path / "draft_package.json"
        with open(package_file, 'w', encoding='utf-8') as f:
            json.dump(drafts, f, ensure_ascii=False, indent=2)
        print(f"📦 完整草稿包: {package_file}")
        
        return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="多平台草稿导出工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 导出到指定平台
  python export_draft.py content.json --platform 搜狐号
  
  # 批量导出所有平台
  python export_draft.py content.json --batch
  
  # 导出到指定目录
  python export_draft.py content.json --batch --output ./drafts/
        """
    )
    
    parser.add_argument("content_file", help="内容JSON文件路径")
    parser.add_argument("--platform", "-p", choices=["搜狐号", "网易号", "快手", "全部"],
                       help="目标平台")
    parser.add_argument("--batch", "-b", action="store_true", help="批量导出所有平台")
    parser.add_argument("--output", "-o", default="./drafts", help="输出目录")
    parser.add_argument("--copy", "-c", action="store_true", help="直接显示复制内容")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.content_file):
        print(f"❌ 文件不存在: {args.content_file}")
        sys.exit(1)
    
    exporter = DraftExporter()
    content = exporter.load_content(args.content_file)
    
    print("\n" + "=" * 50)
    print("📦 GEO内容草稿导出工具")
    print("=" * 50)
    
    if args.batch or args.platform == "全部":
        # 导出所有平台
        drafts = exporter.export_all(content)
        output_dir = exporter.save_draft_package(drafts, args.output, 
                                                 content.get("enterprise_name", "商家"))
        
        print(f"\n✅ 所有平台草稿已导出到: {output_dir}")
        
        if args.copy:
            print("\n" + "-" * 50)
            for platform, draft in drafts.items():
                print(f"\n📋 {platform} 复制内容：")
                print("-" * 50)
                print(draft.get('copy_ready', '')[:500])
                print("...")
    
    elif args.platform:
        # 导出指定平台
        if "搜狐" in args.platform:
            draft = exporter.export_for_souhu(content)
        elif "网易" in args.platform:
            draft = exporter.export_for_wangyi(content)
        elif "快手" in args.platform:
            draft = exporter.export_for_kuaishou(content)
        else:
            print(f"❌ 不支持的平台: {args.platform}")
            sys.exit(1)
        
        print(f"\n📋 {args.platform} 草稿：")
        print("-" * 50)
        print(f"标题: {draft.get('title', '')}")
        print(f"\n正文:\n{draft.get('plain_text', '')[:500]}...")
        print("-" * 50)
        
        # 保存
        output_path = Path(args.output)
        output_path.mkdir(parents=True, exist_ok=True)
        
        platform_name = args.platform.replace("号", "")
        draft_file = output_path / f"draft_{platform_name}.txt"
        
        with open(draft_file, 'w', encoding='utf-8') as f:
            f.write("=" * 50 + "\n")
            f.write(f"平台：{draft['platform']}\n")
            f.write("=" * 50 + "\n\n")
            f.write("【标题】\n")
            f.write(draft.get('title', '') + "\n\n")
            f.write("【正文】\n")
            f.write(draft.get('plain_text', draft.get('full_text', '')) + "\n\n")
            f.write("【标签】\n")
            f.write(', '.join(draft.get('tags', [])) + "\n\n")
            f.write("【一键复制内容】\n")
            f.write("-" * 50 + "\n")
            f.write(draft.get('copy_ready', '') + "\n")
        
        print(f"\n✅ 草稿已保存: {draft_file}")
    
    else:
        print("\n❌ 请指定平台（--platform）或使用 --batch 导出所有平台")


if __name__ == "__main__":
    main()
