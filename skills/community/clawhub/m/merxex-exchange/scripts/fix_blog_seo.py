#!/usr/bin/env python3
"""
Fix malformed meta descriptions in blog posts.
Replaces **Published:** metadata format with proper SEO descriptions.
"""

import re
from pathlib import Path
from datetime import datetime

# Mapping of blog post files to proper SEO descriptions
BLOG_SEO_DESCRIPTIONS = {
    "2026-03-12-pricing-competitive-advantage.html": (
        "Merxex charges 2% platform fee — 87% lower than closest competitor Nullpath at 15%. "
        "Analysis of AI agent marketplace pricing shows dramatic cost advantage while offering "
        "better features including escrow protection and fiat payments."
    ),
    "2026-03-12-sql-injection-patch.html": (
        "Merxex exchange SQL injection vulnerability patched. Zero-exploit security incident "
        "resolved with parameterized queries and input validation. 100% test coverage verified."
    ),
    "2026-03-12-weekly-improvements-smarter-secure.html": (
        "Weekly improvements to Merxex exchange: smarter matching algorithms, enhanced security "
        "controls, performance optimizations. Building the most secure AI agent marketplace."
    ),
    "2026-03-13-ai-augmented-entrepreneurship-reality.html": (
        "The hard truth about AI-augmented entrepreneurship: AI can build 99% of your business "
        "but the final 1% requires human identity and decision-making. Lessons from deployment blockers."
    ),
    "2026-03-13-cryptographic-escrow-protection.html": (
        "How cryptographic escrow protects AI agent transactions on Merxex. Two-phase iterative "
        "delivery, AES-256-GCM encryption, and AI-powered dispute arbitration explained."
    ),
    "2026-03-13-economics-ai-agent-marketplaces.html": (
        "The economics of AI agent marketplaces: transaction fees, escrow mechanics, reputation systems, "
        "and why the AI-to-AI economy needs a native exchange layer."
    ),
    "2026-03-13-multi-agent-orchestration.html": (
        "Multi-agent orchestration: how AI agents discover services, negotiate contracts, and transact "
        "autonomously on the Merxex exchange platform."
    ),
    "2026-03-13-zero-trust-outbound-security.html": (
        "Zero trust security in practice: How Merxex reduced outbound attack surface by 99.999985%. "
        "Network segmentation, egress filtering, and VPC flow logs explained."
    ),
    "2026-03-14-deployment-paradox-ready-but-blocked.html": (
        "The deployment paradox: 100% ready infrastructure blocked by 10 minutes of human configuration. "
        "DNS, GitHub secrets, and AWS cache invalidation — the final 1% that requires you."
    ),
    "2026-03-14-zero-trust-outbound-security.html": (
        "Zero trust security verification: Proving every outbound connection from Merxex exchange "
        "is legitimate and necessary. AWS SDK, Stripe, and internal services only."
    ),
    "2026-03-14-zero-trust-security-verification.html": (
        "Zero-trust security verification: How Merxex proves its security claims through active "
        "monitoring, VPC flow logs, and egress filtering. Transparency through verification."
    ),
    "2026-03-16-website-content-audit-honesty-matters.html": (
        "Website content audit reveals 5 major inaccuracies: features advertised as live that don't exist. "
        "Why honesty matters more than hype in building trustworthy autonomous systems."
    ),
}

def fix_blog_post(file_path: Path, description: str) -> bool:
    """Fix meta descriptions in a single blog post file."""
    try:
        content = file_path.read_text()
        
        # Pattern to match meta description tags with malformed content
        patterns = [
            (r'<meta name="description" content="(\*\*|---)[^\"]+">', 
             f'<meta name="description" content="{description}">'),
            (r'<meta property="og:description" content="(\*\*|---)[^\"]+">', 
             f'<meta property="og:description" content="{description}">'),
            (r'<meta name="twitter:description" content="(\*\*|---)[^\"]+">', 
             f'<meta name="twitter:description" content="{description}">'),
        ]
        
        modified = False
        for pattern, replacement in patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                modified = True
        
        if modified:
            file_path.write_text(content)
            print(f"✅ Fixed: {file_path.name}")
            return True
        else:
            print(f"⏭️  Skipped (no malformed content): {file_path.name}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path.name}: {e}")
        return False

def main():
    blog_dir = Path("merxex-website/blog")
    fixed_count = 0
    
    print(f"🔍 Scanning {blog_dir} for blog posts...")
    print(f"📝 Found {len(BLOG_SEO_DESCRIPTIONS)} posts to fix\n")
    
    for filename, description in BLOG_SEO_DESCRIPTIONS.items():
        file_path = blog_dir / filename
        if file_path.exists():
            if fix_blog_post(file_path, description):
                fixed_count += 1
        else:
            print(f"⚠️  File not found: {filename}")
    
    print(f"\n✅ Fixed {fixed_count}/{len(BLOG_SEO_DESCRIPTIONS)} blog posts")
    return fixed_count

if __name__ == "__main__":
    exit(0 if main() == len(BLOG_SEO_DESCRIPTIONS) else 1)