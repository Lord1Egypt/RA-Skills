import sys
import re
from typing import Optional
import instaloader


def extract_shortcode(url: str) -> Optional[str]:
    """
    Extract the shortcode from an Instagram post or reel URL.

    Examples:
        https://www.instagram.com/p/DRiFkfoiIuC/         → DRiFkfoiIuC
        https://www.instagram.com/reel/DRiFkfoiIuC/      → DRiFkfoiIuC
        https://www.instagram.com/p/DRiFkfoiIuC/?img_index=3  → DRiFkfoiIuC
    """
    match = re.search(r"instagram\.com/(?:p|reel)/([A-Za-z0-9_-]+)", url)
    return match.group(1) if match else None


def scrape_instagram_caption(url: str) -> str:
    """
    Fetch the caption from a public Instagram post or reel URL using Instaloader.

    Args:
        url (str): Instagram post or reel URL

    Returns:
        str: Result string starting with CAPTION: or ERROR:
    """
    # Validate URL
    if not re.match(r"https://(www\.)?instagram\.com/(p|reel)/", url):
        return "ERROR: Invalid Instagram URL. Expected: https://www.instagram.com/p/... or /reel/..."

    # Extract shortcode
    shortcode = extract_shortcode(url)
    if not shortcode:
        return "ERROR: Could not extract shortcode from URL."

    try:
        L = instaloader.Instaloader()

        # Optional: uncomment and add credentials to access private accounts
        # L.login("your_username", "your_password")

        post = instaloader.Post.from_shortcode(L.context, shortcode)

        caption = post.caption

        if not caption or caption.strip() == "":
            return "CAPTION: (No caption on this post)"

        # Include some useful metadata alongside the caption
        post_type = post.typename  # GraphImage, GraphVideo, GraphSidecar
        likes = post.likes
        owner = post.owner_username

        result = (
            f"CAPTION: {caption.strip()}\n\n"
            f"---\n"
            f"Owner   : @{owner}\n"
            f"Type    : {post_type}\n"
            f"Likes   : {likes}\n"
            f"Shortcode: {shortcode}"
        )
        return result

    except instaloader.exceptions.InstaloaderException as e:
        error_msg = str(e)
        if "login" in error_msg.lower() or "private" in error_msg.lower():
            return "ERROR: This post is private or requires Instagram login to access."
        elif "not found" in error_msg.lower() or "404" in error_msg:
            return "ERROR: Post not found. It may have been deleted or the URL is incorrect."
        else:
            return f"ERROR: Instaloader failed — {error_msg}"

    except Exception as e:
        return f"ERROR: Unexpected error — {str(e)}"


def main(url: str = None) -> str:
    """
    Entry point — supports CLI, direct call, and OpenClaw skill tool use.

    Args:
        url (str): Instagram URL. If None, reads from stdin or sys.argv.

    Returns:
        str: CAPTION: <text> or ERROR: <reason>
    """
    if not url:
        url = sys.argv[1] if len(sys.argv) > 1 else input("Enter Instagram URL: ").strip()

    result = scrape_instagram_caption(url)
    return result


if __name__ == "__main__":
    output = main()
    print(output)