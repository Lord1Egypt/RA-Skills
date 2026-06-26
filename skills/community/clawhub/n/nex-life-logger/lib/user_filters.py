"""
Nex Life Logger - User-configurable Filters
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

Loads, saves, and provides access to all user-customizable filter lists.
Stored as a single JSON file in the data directory.
"""
import json
import logging
import re
from pathlib import Path

log = logging.getLogger("life-logger.user-filters")

_FILTERS_PATH = None

_DEFAULTS = {
    "productive_domains": [
        "github.com", "gitlab.com", "bitbucket.org",
        "stackoverflow.com", "stackexchange.com",
        "docs.python.org", "docs.anthropic.com", "platform.openai.com",
        "developer.mozilla.org", "mdn.mozilla.org",
        "arxiv.org", "paperswithcode.com",
        "huggingface.co", "kaggle.com",
        "medium.com",
        "dev.to", "hashnode.dev",
        "replit.com", "codepen.io", "codesandbox.io",
        "figma.com", "canva.com",
        "notion.so", "obsidian.md",
        "vercel.com", "netlify.com", "render.com",
        "aws.amazon.com", "cloud.google.com", "azure.microsoft.com",
        "npmjs.com", "pypi.org", "crates.io",
        "udemy.com", "coursera.org", "edx.org",
        "leetcode.com", "hackerrank.com",
        "blender.org",
    ],
    "non_productive_domains": [
        "cnn.com", "foxnews.com", "msnbc.com", "bbc.com", "bbc.co.uk",
        "nytimes.com", "washingtonpost.com", "theguardian.com",
        "politico.com", "reuters.com", "apnews.com",
        "huffpost.com", "dailymail.co.uk", "nypost.com",
        "news.google.com", "news.yahoo.com",
        "breitbart.com", "thehill.com", "vox.com",
        "netflix.com", "hulu.com", "disneyplus.com", "max.com",
        "twitch.tv", "tiktok.com",
        "reddit.com",
        "9gag.com", "imgur.com", "buzzfeed.com",
        "instagram.com", "twitter.com", "x.com",
        "facebook.com",
        "espn.com", "sports.yahoo.com", "cbssports.com",
        "tmz.com", "eonline.com", "people.com",
    ],
    "productive_keywords": [
        r"\bai\b", r"\bartificial.?intelligence\b", r"\bmachine.?learning\b",
        r"\bdeep.?learning\b", r"\bneural.?net", r"\bllm\b", r"\bgpt\b",
        r"\bclaude\b", r"\btransformer", r"\bfine.?tun", r"\brag\b",
        r"\bprompt.?engineer", r"\bagent", r"\bmodel\b.*\btrain",
        r"\bdiffusion\b", r"\bstable.?diffusion\b", r"\bmidjourney\b",
        r"\bcomfy.?ui\b", r"\blangchain\b", r"\bllamaindex\b",
        r"\bvector.?database\b", r"\bembedding",
        r"\bpython\b", r"\bjavascript\b", r"\btypescript\b", r"\brust\b",
        r"\breact\b", r"\bnextjs\b", r"\bnode\.?js\b", r"\bvue\b", r"\bsvelte\b",
        r"\bapi\b", r"\bbackend\b", r"\bfrontend\b", r"\bfull.?stack\b",
        r"\bdocker\b", r"\bkubernetes\b", r"\bdevops\b",
        r"\bgit\b", r"\bgithub\b", r"\bopen.?source\b",
        r"\btutorial\b", r"\bcoding\b", r"\bprogramming\b",
        r"\bdebug", r"\brefactor", r"\barchitect",
        r"\bdatabase\b", r"\bsql\b", r"\bpostgres\b", r"\bmongo\b",
        r"\bfigma\b", r"\bblender\b", r"\b3d.?model", r"\bui.?design\b",
        r"\bux\b", r"\bdesign.?system\b", r"\bprototyp",
        r"\bstartup\b", r"\bsaas\b", r"\bproduct\b.*\bbuild",
        r"\bautomation\b", r"\bno.?code\b", r"\blow.?code\b",
        r"\bworkflow\b", r"\bproductivity\b",
        r"\bcourse\b", r"\blearn", r"\bhow.?to\b", r"\bguide\b",
        r"\bdocumentation\b", r"\btutorial\b",
    ],
    "non_productive_keywords": [
        r"\bpolitics\b", r"\bpolitician\b", r"\belection\b", r"\bdemocrat\b",
        r"\brepublican\b", r"\btrump\b", r"\bbiden\b", r"\bcongress\b",
        r"\bsenate\b", r"\bparliament\b", r"\bbrexit\b",
        r"\bleft.?wing\b", r"\bright.?wing\b", r"\bconservative\b", r"\bliberal\b",
        r"\bbreaking.?news\b", r"\bheadlines?\b", r"\bscandal\b",
        r"\bprotest\b", r"\briot\b", r"\bwar\b(?!ning)",
        r"\binvasion\b", r"\bconflict\b", r"\bcrisis\b",
        r"\bmovie\b", r"\bnetflix\b", r"\btv.?show\b", r"\bseries\b",
        r"\btrailer\b", r"\brecap\b", r"\breview\b.*\b(movie|show|series|film)\b",
        r"\bcelebrit", r"\bgossip\b", r"\btabloid\b",
        r"\bfunny\b", r"\bprank\b", r"\bfail\b", r"\bmeme\b",
        r"\bvlog\b", r"\bdaily.?vlog\b", r"\bchallenge\b",
        r"\bnba\b", r"\bnfl\b", r"\bfifa\b", r"\bpremier.?league\b",
        r"\bchampions.?league\b", r"\bworld.?cup\b",
        r"\bgoal\b.*\b(score|match)\b", r"\bhighlight\b.*\b(game|match)\b",
        r"\bmusic.?video\b", r"\bofficial.?video\b", r"\blyric\b",
        r"\blive.?performance\b", r"\bconcert\b",
    ],
    "tool_patterns": [
        [r"\bpython\b", "Python", "language"],
        [r"\bjavascript\b", "JavaScript", "language"],
        [r"\btypescript\b", "TypeScript", "language"],
        [r"\brust\b", "Rust", "language"],
        [r"\bjava\b(?!script)", "Java", "language"],
        [r"\bc\+\+\b", "C++", "language"],
        [r"\bc#\b|csharp", "C#", "language"],
        [r"\bgo\b(?:lang)?", "Go", "language"],
        [r"\bswift\b", "Swift", "language"],
        [r"\bkotlin\b", "Kotlin", "language"],
        [r"\bhtml\b", "HTML", "language"],
        [r"\bcss\b", "CSS", "language"],
        [r"\bsql\b", "SQL", "language"],
        [r"\breact\b", "React", "tool"],
        [r"\bnext\.?js\b", "Next.js", "tool"],
        [r"\bvue\.?js?\b", "Vue", "tool"],
        [r"\bsvelte\b", "Svelte", "tool"],
        [r"\bangular\b", "Angular", "tool"],
        [r"\bnode\.?js\b", "Node.js", "tool"],
        [r"\bdjango\b", "Django", "tool"],
        [r"\bflask\b", "Flask", "tool"],
        [r"\bfastapi\b", "FastAPI", "tool"],
        [r"\bdocker\b", "Docker", "tool"],
        [r"\bkubernetes\b|\bk8s\b", "Kubernetes", "tool"],
        [r"\bgit\b(?!hub)", "Git", "tool"],
        [r"\bgithub\b", "GitHub", "tool"],
        [r"\bvs\s?code\b|\bvisual\s?studio\s?code\b", "VS Code", "tool"],
        [r"\bfigma\b", "Figma", "tool"],
        [r"\bblender\b", "Blender", "tool"],
        [r"\bphotoshop\b", "Photoshop", "tool"],
        [r"\btailwind\b", "Tailwind CSS", "tool"],
        [r"\bwebpack\b", "Webpack", "tool"],
        [r"\bvite\b", "Vite", "tool"],
        [r"\bpostgres\b|\bpostgresql\b", "PostgreSQL", "tool"],
        [r"\bmongo\b(?:db)?", "MongoDB", "tool"],
        [r"\bredis\b", "Redis", "tool"],
        [r"\baws\b", "AWS", "tool"],
        [r"\bazure\b", "Azure", "tool"],
        [r"\bgcp\b|\bgoogle\s?cloud\b", "Google Cloud", "tool"],
        [r"\bvercel\b", "Vercel", "tool"],
        [r"\bnetlify\b", "Netlify", "tool"],
        [r"\bnpm\b", "npm", "tool"],
        [r"\bpip\b", "pip", "tool"],
        [r"\bclaude\b", "Claude", "tool"],
        [r"\bgpt\b", "GPT", "tool"],
        [r"\bopenai\b", "OpenAI", "tool"],
        [r"\bgemini\b", "Gemini", "tool"],
        [r"\bllama\b", "LLaMA", "tool"],
        [r"\bmistral\b", "Mistral", "tool"],
        [r"\blangchain\b", "LangChain", "tool"],
        [r"\bllamaindex\b", "LlamaIndex", "tool"],
        [r"\bhugging\s?face\b", "Hugging Face", "tool"],
        [r"\bstable\s?diffusion\b", "Stable Diffusion", "tool"],
        [r"\bmidjourney\b", "Midjourney", "tool"],
        [r"\bcomfy\s?ui\b", "ComfyUI", "tool"],
        [r"\bunity\b", "Unity", "tool"],
        [r"\bunreal\b", "Unreal Engine", "tool"],
        [r"\bnotion\b", "Notion", "tool"],
        [r"\bobsidian\b", "Obsidian", "tool"],
    ],
    "topic_patterns": [
        [r"\bmachine\s?learning\b", "Machine Learning", "topic"],
        [r"\bdeep\s?learning\b", "Deep Learning", "topic"],
        [r"\bartificial\s?intelligence\b|\b(?:ai)\b", "AI", "topic"],
        [r"\bneural\s?net\w*\b", "Neural Networks", "topic"],
        [r"\btransformer\w*\b", "Transformers", "topic"],
        [r"\bllm\b", "LLMs", "topic"],
        [r"\bfine[\s-]?tun\w*\b", "Fine-tuning", "topic"],
        [r"\brag\b", "RAG", "topic"],
        [r"\bprompt\s?engineer\w*\b", "Prompt Engineering", "topic"],
        [r"\bvector\s?database\b|\bvector\s?db\b", "Vector Databases", "topic"],
        [r"\bembedding\w*\b", "Embeddings", "topic"],
        [r"\bapi\b", "API Development", "topic"],
        [r"\bbackend\b", "Backend", "topic"],
        [r"\bfrontend\b", "Frontend", "topic"],
        [r"\bfull[\s-]?stack\b", "Full-stack", "topic"],
        [r"\bdevops\b", "DevOps", "topic"],
        [r"\bci[\s/]?cd\b", "CI/CD", "topic"],
        [r"\bmicroservice\w*\b", "Microservices", "topic"],
        [r"\bui[\s/]?ux\b|\buser\s?interface\b|\buser\s?experience\b", "UI/UX Design", "topic"],
        [r"\bdesign\s?system\b", "Design Systems", "topic"],
        [r"\b3d\s?model\w*\b", "3D Modeling", "topic"],
        [r"\bweb\s?scraping\b", "Web Scraping", "topic"],
        [r"\bautomation\b", "Automation", "topic"],
        [r"\bdata\s?science\b", "Data Science", "topic"],
        [r"\bdata\s?engineer\w*\b", "Data Engineering", "topic"],
        [r"\bcyber\s?security\b|\bsecurity\b", "Security", "topic"],
        [r"\bcryptograph\w*\b", "Cryptography", "topic"],
        [r"\bblockchain\b", "Blockchain", "topic"],
        [r"\bweb3\b", "Web3", "topic"],
        [r"\bstartup\b", "Startup", "topic"],
        [r"\bsaas\b", "SaaS", "topic"],
        [r"\bopen[\s-]?source\b", "Open Source", "topic"],
        [r"\btutorial\b", "Tutorial", "topic"],
        [r"\bcourse\b", "Course", "topic"],
        [r"\bdocumentation\b|\bdocs\b", "Documentation", "topic"],
        [r"\bdebug\w*\b", "Debugging", "topic"],
        [r"\brefactor\w*\b", "Refactoring", "topic"],
        [r"\btesting\b|\bunit\s?test\b", "Testing", "topic"],
        [r"\bperformance\b|\boptimiz\w*\b", "Performance", "topic"],
        [r"\baccessibility\b|\ba11y\b", "Accessibility", "topic"],
        [r"\bresponsive\b", "Responsive Design", "topic"],
        [r"\banimation\b", "Animation", "topic"],
        [r"\bgame\s?dev\w*\b", "Game Development", "topic"],
        [r"\bmobile\s?dev\w*\b|\bios\b|\bandroid\b", "Mobile Development", "topic"],
        [r"\bcloud\s?computing\b", "Cloud Computing", "topic"],
        [r"\bserverless\b", "Serverless", "topic"],
        [r"\bcontainer\w*\b", "Containers", "topic"],
    ],
    "domain_keyword_map": {
        "github.com": "GitHub", "gitlab.com": "GitLab",
        "stackoverflow.com": "StackOverflow",
        "arxiv.org": "arXiv", "huggingface.co": "Hugging Face",
        "kaggle.com": "Kaggle", "figma.com": "Figma",
        "vercel.com": "Vercel", "netlify.com": "Netlify",
        "medium.com": "Medium", "dev.to": "Dev.to",
        "udemy.com": "Udemy", "coursera.org": "Coursera",
        "leetcode.com": "LeetCode", "codepen.io": "CodePen",
        "replit.com": "Replit", "npmjs.com": "npm",
        "pypi.org": "PyPI", "docs.python.org": "Python Docs",
    },
    "process_keyword_map": {
        "code.exe": "VS Code", "Code.exe": "VS Code",
        "devenv.exe": "Visual Studio", "pycharm64.exe": "PyCharm",
        "idea64.exe": "IntelliJ IDEA", "webstorm64.exe": "WebStorm",
        "blender.exe": "Blender", "figma.exe": "Figma",
        "unity.exe": "Unity", "unrealengine.exe": "Unreal Engine",
        "obsidian.exe": "Obsidian", "notion.exe": "Notion",
        "postman.exe": "Postman", "insomnia.exe": "Insomnia",
        "WindowsTerminal.exe": "Windows Terminal",
        "powershell.exe": "PowerShell", "cmd.exe": "Terminal",
        "chrome.exe": "Chrome", "firefox.exe": "Firefox",
        "msedge.exe": "Edge", "brave.exe": "Brave",
    },
    "chat_blocked_domains": [
        "web.whatsapp.com", "www.messenger.com", "messenger.com",
        "www.facebook.com/messages",
        "web.telegram.org", "telegram.org",
        "discord.com", "discordapp.com",
        "app.slack.com", "slack.com",
        "signal.org",
        "teams.microsoft.com", "teams.live.com",
        "web.skype.com",
        "messages.google.com",
        "app.element.io", "element.io",
        "viber.com", "line.me",
        "web.wechat.com", "web.snapchat.com",
    ],
    "chat_url_patterns": [
        "/messages", "/direct", "/chat", "/dm/",
        "/dms", "/conversations", "/inbox", "/messaging",
    ],
    "chat_window_keywords": [
        "whatsapp", "telegram", "discord", "slack", "signal",
        "teams", "messenger", "skype", "viber", "element",
        "imessage", "messages", "wechat",
    ],
    "sensitive_window_keywords": [
        "password", "passwd", "credential", "keychain", "vault",
        "1password", "lastpass", "bitwarden", "keepass", "dashlane",
        "private browsing", "incognito", "inprivate",
        "bank", "banking",
    ],
}

_cache = None
_compiled_tool_patterns = None
_compiled_topic_patterns = None
_compiled_productive_kw = None
_compiled_non_productive_kw = None


def init(data_dir):
    global _FILTERS_PATH
    _FILTERS_PATH = data_dir / "user_filters.json"
    reload()


def reload():
    global _cache, _compiled_tool_patterns, _compiled_topic_patterns
    global _compiled_productive_kw, _compiled_non_productive_kw
    _cache = _load_from_disk()
    _compiled_tool_patterns = None
    _compiled_topic_patterns = None
    _compiled_productive_kw = None
    _compiled_non_productive_kw = None


def _load_from_disk():
    if _FILTERS_PATH and _FILTERS_PATH.exists():
        try:
            import copy
            user_data = json.loads(_FILTERS_PATH.read_text("utf-8"))
            merged = {}
            for key, default_val in _DEFAULTS.items():
                if key in user_data:
                    merged[key] = user_data[key]
                else:
                    merged[key] = copy.deepcopy(default_val)
            return merged
        except Exception as e:
            log.warning("Failed to load user_filters.json: %s, using defaults", e)
    import copy
    return copy.deepcopy(_DEFAULTS)


def save(filters):
    global _cache
    if not _FILTERS_PATH:
        return {"error": "Filter system not initialized"}
    try:
        for key in ("productive_keywords", "non_productive_keywords"):
            if key in filters:
                for p in filters[key]:
                    re.compile(p, re.IGNORECASE)
        for key in ("tool_patterns", "topic_patterns"):
            if key in filters:
                for entry in filters[key]:
                    if len(entry) != 3:
                        return {"error": "Each %s entry must be [regex, name, category]" % key}
                    re.compile(entry[0], re.IGNORECASE)
        _FILTERS_PATH.parent.mkdir(parents=True, exist_ok=True)
        _FILTERS_PATH.write_text(json.dumps(filters, indent=2, ensure_ascii=False), "utf-8")
        reload()
        return {"ok": True, "message": "Filters saved and reloaded"}
    except re.error as e:
        return {"error": "Invalid regex pattern: %s" % e}
    except Exception as e:
        return {"error": str(e)}


def reset_to_defaults():
    global _cache
    if _FILTERS_PATH and _FILTERS_PATH.exists():
        try:
            _FILTERS_PATH.unlink()
        except Exception as e:
            return {"error": str(e)}
    reload()
    return {"ok": True, "message": "Filters reset to defaults"}


def _ensure_loaded():
    global _cache
    if _cache is None:
        _cache = _load_from_disk()


def get(key):
    _ensure_loaded()
    return _cache.get(key, _DEFAULTS.get(key))


def get_all():
    _ensure_loaded()
    return dict(_cache)


def get_compiled_tool_patterns():
    global _compiled_tool_patterns
    if _compiled_tool_patterns is None:
        _compiled_tool_patterns = []
        for entry in get("tool_patterns"):
            try:
                _compiled_tool_patterns.append(
                    (re.compile(entry[0], re.IGNORECASE), entry[1], entry[2])
                )
            except re.error:
                log.warning("Skipping invalid tool pattern: %s", entry[0])
    return _compiled_tool_patterns


def get_compiled_topic_patterns():
    global _compiled_topic_patterns
    if _compiled_topic_patterns is None:
        _compiled_topic_patterns = []
        for entry in get("topic_patterns"):
            try:
                _compiled_topic_patterns.append(
                    (re.compile(entry[0], re.IGNORECASE), entry[1], entry[2])
                )
            except re.error:
                log.warning("Skipping invalid topic pattern: %s", entry[0])
    return _compiled_topic_patterns


def get_compiled_productive_keywords():
    global _compiled_productive_kw
    if _compiled_productive_kw is None:
        _compiled_productive_kw = []
        for p in get("productive_keywords"):
            try:
                _compiled_productive_kw.append(re.compile(p, re.IGNORECASE))
            except re.error:
                log.warning("Skipping invalid productive keyword pattern: %s", p)
    return _compiled_productive_kw


def get_compiled_non_productive_keywords():
    global _compiled_non_productive_kw
    if _compiled_non_productive_kw is None:
        _compiled_non_productive_kw = []
        for p in get("non_productive_keywords"):
            try:
                _compiled_non_productive_kw.append(re.compile(p, re.IGNORECASE))
            except re.error:
                log.warning("Skipping invalid non-productive keyword pattern: %s", p)
    return _compiled_non_productive_kw
