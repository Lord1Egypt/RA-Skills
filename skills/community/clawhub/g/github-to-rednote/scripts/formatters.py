#!/usr/bin/env python3
"""
RedNote (小红书) formatting utilities - Enhanced version.
Optimized for mobile reading and RedNote platform.
"""

import re
import textwrap
from typing import List, Optional


class RedNoteFormatter:
    """Format content for RedNote style with enhanced features."""
    
    # Common tech hashtags in Chinese
    DEFAULT_HASHTAGS = [
        "#技术分享",
        "#开源项目",
        "#程序员",
        "#GitHub",
        "#开发工具",
        "#代码学习",
        "#技术干货",
        "#编程入门",
        "#工具推荐",
        "#效率工具"
    ]
    
    # Language-specific hashtags
    LANGUAGE_TAGS = {
        'Python': ['#Python', '#Python学习'],
        'JavaScript': ['#JavaScript', '#JS', '#前端开发'],
        'TypeScript': ['#TypeScript', '#TS', '#前端开发'],
        'Java': ['#Java', '#Java开发'],
        'Go': ['#Go', '#Golang', '#Go语言'],
        'Rust': ['#Rust', '#Rust语言'],
        'C++': ['#C++', '#CPP'],
        'C': ['#C语言'],
        'Ruby': ['#Ruby'],
        'PHP': ['#PHP'],
        'Swift': ['#Swift', '#iOS开发'],
        'Kotlin': ['#Kotlin', '#Android开发'],
    }
    
    # Emoji decorations by section
    EMOJIS = {
        'title': ['🔥', '⚡️', '🚀', '💎', '⭐', '🎯', '💡'],
        'section': ['📌', '💡', '📍', '✨', '🎯', '📋', '🔍'],
        'list': ['▸', '•', '→', '➤', '★', '✓', '▪'],
        'highlight': ['🔥', '⚡️', '💪', '🚀', '✅', '💯', '🌟'],
        'code': ['💻', '⌨️', '🖥️', '🔧', '⚙️', '📝'],
        'star': ['⭐', '🌟', '💫', '✨'],
        'warning': ['⚠️', '❗', '🔔', '💢'],
        'tip': ['💡', '📌', '✏️', '📝', '🎓'],
        'stats': ['📊', '📈', '📉'],
        'link': ['🔗', '🌐', '📎'],
        'user': ['👤', '👥', '🧑‍💻', '👨‍💻', '👩‍💻'],
        'time': ['⏰', '📅', '🕐'],
        'tag': ['🏷️', '📌', '#️⃣']
    }
    
    # Mobile-friendly line width
    MAX_LINE_WIDTH = 32
    
    @staticmethod
    def add_title_emoji(title: str, emoji: str = None, randomize: bool = False) -> str:
        """Add emoji to title."""
        if not emoji:
            if randomize:
                import random
                emoji = random.choice(RedNoteFormatter.EMOJIS['title'])
            else:
                emoji = RedNoteFormatter.EMOJIS['title'][0]
        return f"{emoji} {title}"
    
    @staticmethod
    def format_section_header(text: str, emoji: str = None) -> str:
        """Format section header with emoji."""
        if not emoji:
            emoji = RedNoteFormatter.EMOJIS['section'][0]
        return f"\n{emoji} **{text}**\n"
    
    @staticmethod
    def format_bullet(text: str, emoji: str = "▸", indent: int = 0) -> str:
        """Format bullet point with optional indent."""
        indent_str = "  " * indent
        return f"{indent_str}{emoji} {text}"
    
    @staticmethod
    def format_highlight(text: str, emoji: str = "🔥") -> str:
        """Format highlighted text."""
        return f"{emoji} **{text}** {emoji}"
    
    @staticmethod
    def format_code_block(code: str, language: str = "") -> str:
        """Format code block for mobile."""
        # Limit code block width for mobile
        lines = code.strip().split('\n')
        max_width = 30  # Mobile-friendly width
        
        formatted_lines = []
        for line in lines:
            if len(line) > max_width:
                # Truncate long lines with ellipsis
                line = line[:max_width-3] + "..."
            formatted_lines.append(line)
        
        code = '\n'.join(formatted_lines)
        return f"\n💻 代码示例:\n```{language}\n{code}\n```\n"
    
    @staticmethod
    def format_inline_code(code: str) -> str:
        """Format inline code."""
        return f"`{code}`"
    
    @staticmethod
    def format_repo_card(repo_data: dict) -> str:
        """Format a repository card for RedNote."""
        lines = []
        
        # Header with emoji
        name = repo_data.get('repo', 'Unknown')
        lines.append(f"📦 **{name}**")
        
        # Description (truncated)
        desc = repo_data.get('description', '暂无描述')
        if desc:
            lines.append(RedNoteFormatter.truncate_text(desc, 60))
        
        # Stats line - Stars smart display rule
        stars = repo_data.get('stars', 0)
        forks = repo_data.get('forks', 0)
        lang = repo_data.get('language', 'Unknown')
        
        stars_str = RedNoteFormatter.format_stars_display(stars)
        lines.append(f"{stars_str}🍴 {forks:,} | 💻 {lang}" if stars_str else f"🍴 {forks:,} | 💻 {lang}")
        
        return '\n'.join(lines)
    
    @staticmethod
    def format_stars_display(stars: int) -> str:
        """Format stars count with smart display rule (>= 100 only)."""
        if stars >= 100:
            if stars >= 1000:
                return f"⭐ {stars/1000:.1f}k stars | "
            else:
                return f"⭐ {stars} stars | "
        # stars < 100 不显示
        return ""
    
    @staticmethod
    def format_repo_stats(stars: int, forks: int, language: str) -> str:
        """Format repository stats line with smart stars display."""
        stars_str = RedNoteFormatter.format_stars_display(stars)
        if stars_str:
            return f"{stars_str}🍴 {forks:,} | 💻 {language}"
        else:
            return f"🍴 {forks:,} | 💻 {language}"
    
    @staticmethod
    def format_stats_box(repo_data: dict) -> str:
        """Format a nice stats box."""
        lines = ["📊 项目数据"]
        
        stats = [
            ("⭐ Stars", repo_data.get('stars', 0)),
            ("🍴 Forks", repo_data.get('forks', 0)),
            ("👁️ Watchers", repo_data.get('watchers', 0)),
            ("🐛 Issues", repo_data.get('open_issues', 0)),
        ]
        
        for label, value in stats:
            lines.append(f"  {label}: {value:,}")
        
        # Add language breakdown if available
        languages = repo_data.get('languages', {})
        if languages:
            total = sum(languages.values())
            lines.append(f"\n  💻 主要语言: {repo_data.get('language', 'Unknown')}")
            # Top 3 languages
            for lang, bytes_count in sorted(languages.items(), key=lambda x: x[1], reverse=True)[:3]:
                pct = bytes_count / total * 100
                lines.append(f"    • {lang}: {pct:.1f}%")
        
        return '\n'.join(lines)
    
    @staticmethod
    def format_release_card(release: dict) -> str:
        """Format a release info card."""
        tag = release.get('tag_name', 'N/A')
        name = release.get('name', 'No name')
        published = release.get('published_at', '')[:10]  # Just the date
        
        lines = [
            f"🚀 {tag}",
            f"  {name}",
        ]
        if published:
            lines.append(f"  📅 {published}")
        
        return '\n'.join(lines)
    
    @staticmethod
    def format_contributor_list(contributors: List[dict], limit: int = 5) -> str:
        """Format contributor list."""
        if not contributors:
            return ""
        
        lines = [f"👥 贡献者 ({len(contributors)} 人)"]
        
        for c in contributors[:limit]:
            login = c.get('login', 'Unknown')
            count = c.get('contributions', 0)
            lines.append(f"  • @{login}: {count} 次提交")
        
        return '\n'.join(lines)
    
    @staticmethod
    def add_hashtags(repo_data: dict = None, extra_tags: List[str] = None,
                     include_default: bool = True) -> str:
        """
        Generate relevant hashtags based on repository data.
        
        Args:
            repo_data: Repository data for context-aware tags
            extra_tags: Additional custom tags
            include_default: Include default tech tags
        """
        hashtags = set()
        
        # Add repo topics
        if repo_data:
            for topic in repo_data.get('topics', [])[:5]:
                hashtags.add(f"#{topic}")
            
            # Add language tags
            lang = repo_data.get('language', '')
            if lang and lang in RedNoteFormatter.LANGUAGE_TAGS:
                for tag in RedNoteFormatter.LANGUAGE_TAGS[lang]:
                    hashtags.add(tag)
            elif lang:
                hashtags.add(f"#{lang}")
        
        # Add extra tags
        if extra_tags:
            for tag in extra_tags:
                if not tag.startswith('#'):
                    tag = f"#{tag}"
                hashtags.add(tag)
        
        # Add defaults
        if include_default:
            hashtags.update(RedNoteFormatter.DEFAULT_HASHTAGS)
        
        # Limit total tags
        hashtags = list(hashtags)[:15]
        
        return " ".join(hashtags)
    
    @staticmethod
    def format_repo_stats(stars: int, forks: int, language: str) -> str:
        """Format repository stats line."""
        return f"⭐ {stars:,} | 🍴 {forks:,} | 💻 {language}"
    
    @staticmethod
    def add_divider(style: str = "simple") -> str:
        """Add visual divider."""
        if style == "simple":
            return "─" * 20
        elif style == "double":
            return "═" * 20
        elif style == "star":
            return "✦ " * 10
        elif style == "blank":
            return ""
        return "─" * 20
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
        """Truncate text for preview."""
        if not text:
            return ""
        if len(text) <= max_length:
            return text
        return text[:max_length-len(suffix)] + suffix
    
    @staticmethod
    def wrap_text(text: str, width: int = 30) -> str:
        """Wrap text for mobile display."""
        lines = []
        for paragraph in text.split('\n'):
            if paragraph.strip():
                wrapped = textwrap.fill(paragraph, width=width)
                lines.append(wrapped)
            else:
                lines.append('')
        return '\n'.join(lines)
    
    @staticmethod
    def clean_for_rednote(text: str) -> str:
        """Clean text for RedNote format (remove problematic chars)."""
        if not text:
            return ""
        
        # Remove excessive newlines
        text = re.sub(r'\n{4,}', '\n\n\n', text)
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+?>', '', text)
        
        # Remove markdown tables (not supported well on mobile)
        text = re.sub(r'\|[^\n]+\|', '', text)
        
        # Remove images (we'll handle them separately)
        text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'[图片: \1]', text)
        
        # Clean up excessive spaces
        text = re.sub(r' {2,}', ' ', text)
        
        # Remove URLs in favor of cleaner text
        text = re.sub(r'https?://[^\s]+', '[链接]', text)
        
        return text.strip()
    
    @staticmethod
    def extract_key_points(readme: str, max_points: int = 5) -> List[str]:
        """Extract key points from README for bullet list."""
        points = []
        
        # Look for feature lists
        feature_patterns = [
            r'[#*]\s*Features?\s*\n((?:[-*]\s*[^\n]+\n?)+)',
            r'[#*]\s*Key\s+Features?\s*\n((?:[-*]\s*[^\n]+\n?)+)',
            r'(?i)(?:features?|highlights?):\s*\n((?:[-*]\s*[^\n]+\n?)+)'
        ]
        
        for pattern in feature_patterns:
            matches = re.findall(pattern, readme)
            for match in matches:
                for line in match.strip().split('\n'):
                    line = line.strip().lstrip('-*').strip()
                    if line and len(line) > 10:
                        points.append(line)
                if points:
                    break
            if points:
                break
        
        # Limit and clean points
        points = points[:max_points]
        return [RedNoteFormatter.truncate_text(p, 80) for p in points]


def format_rednote_article(content: str, title: str, repo_data: dict = None,
                          tags: List[str] = None, include_header: bool = True,
                          include_footer: bool = True) -> str:
    """
    Apply full RedNote formatting to article content.
    
    Args:
        content: Raw article content
        title: Article title
        repo_data: Repository data for context
        tags: Additional hashtags
        include_header: Include title header
        include_footer: Include hashtags footer
    
    Returns:
        Formatted RedNote article
    """
    formatter = RedNoteFormatter()
    parts = []
    
    # Title with emoji
    if include_header:
        parts.append(formatter.add_title_emoji(title))
        parts.append(formatter.add_divider())
    
    # Clean and add content
    content = formatter.clean_for_rednote(content)
    parts.append(content)
    
    # Add hashtags
    if include_footer:
        parts.append(formatter.add_divider())
        parts.append(formatter.add_hashtags(repo_data, tags))
    
    return "\n".join(parts)


def format_quick_card(repo_data: dict) -> str:
    """Generate a quick reference card for a repository."""
    formatter = RedNoteFormatter()
    
    parts = []
    
    # Title
    title = f"{repo_data.get('repo', 'Project')} - 快速了解"
    parts.append(formatter.add_title_emoji(title, emoji='⚡'))
    
    # One-liner
    desc = repo_data.get('description', '暂无描述')
    parts.append(f"\n💡 {desc}\n")
    
    # Stats box
    parts.append(formatter.format_stats_box(repo_data))
    
    # Links
    parts.append(formatter.format_section_header("🔗 链接"))
    parts.append(formatter.format_bullet(f"GitHub: {repo_data.get('url', 'N/A')}"))
    if repo_data.get('homepage'):
        parts.append(formatter.format_bullet(f"官网: {repo_data.get('homepage')}"))
    
    # Hashtags
    parts.append(formatter.add_divider())
    parts.append(formatter.add_hashtags(repo_data))
    
    return "\n".join(parts)


if __name__ == "__main__":
    # Test formatting
    formatter = RedNoteFormatter()
    
    print("=== RedNote Formatting Tests ===\n")
    
    print(formatter.add_title_emoji("Awesome Project"))
    print(formatter.format_section_header("Key Features"))
    print(formatter.format_bullet("Fast and lightweight"))
    print(formatter.format_bullet("Easy to use", indent=1))
    print(formatter.format_highlight("Star this repo!"))
    print(formatter.format_repo_stats(15000, 1200, "Python"))
    print(formatter.add_divider())
    
    # Test stats box
    test_repo = {
        'repo': 'test-project',
        'description': 'A test project for demonstration',
        'stars': 12345,
        'forks': 678,
        'watchers': 890,
        'open_issues': 42,
        'language': 'Python',
        'languages': {'Python': 8000, 'JavaScript': 1500, 'HTML': 500},
        'url': 'https://github.com/test/test-project',
        'homepage': 'https://test-project.com',
        'topics': ['python', 'web', 'api']
    }
    
    print("\n--- Stats Box ---")
    print(formatter.format_stats_box(test_repo))
    
    print("\n--- Quick Card ---")
    print(format_quick_card(test_repo))
    
    print("\n--- Hashtags ---")
    print(formatter.add_hashtags(test_repo))
