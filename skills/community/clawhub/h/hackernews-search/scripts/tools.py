from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def search_posts(
    query: str,
    tags: Optional[null] = None,
    numericFilters: Optional[null] = None,
    page: Optional[float] = 0.0,
    hitsPerPage: Optional[float] = 20.0
) -> Dict[str, Any]:
    """
    Search HackerNews for stories, comments, and other content by keyword.
	
Supports:
- Keyword search across titles, text, and authors
- Tag filtering (story, comment, poll, show_hn, ask_hn, front_page, author_USERNAME)
- Numeric filters for points, comments, and dates
- Pagination with customizable results per page
- Advanced filtering with OR logic and multiple conditions

Basic Examples:
- Search for AI stories: { "query": "AI", "tags": ["story"] }
- Find popular posts: { "query": "Python", "numericFilters": ["points>=100"] }
- Filter by author: { "query": "startup", "tags": ["author_pg"] }
- Date range: { "query": "startup", "numericFilters": ["created_at_i>1640000000"] }

Advanced Filtering Examples:
- High engagement posts: { "query": "programming", "numericFilters": ["points>=100", "num_comments>=50"] }
- OR logic for tags: { "query": "web", "tags": ["(story,poll)"] } - returns stories OR polls
- Author with filters: { "query": "", "tags": ["author_pg", "story"], "numericFilters": ["points>=50"] }
- Multiple conditions: { "query": "AI", "tags": ["story"], "numericFilters": ["points>=200", "num_comments>=100"] }

Numeric Filter Operators: < (less than), <= (less than or equal), = (equal), >= (greater than or equal), > (greater than)
Numeric Filter Fields: points, num_comments, created_at_i (Unix timestamp)

Tag Syntax:
- Single tag: ["story"] - only stories
- Multiple tags (AND): ["story", "show_hn"] - stories that are also show_hn
- OR logic: ["(story,poll)"] - stories OR polls
- Author filter: ["author_USERNAME"] - posts by specific author

Returns paginated results with hits, total count, and page information.
    
    Args:
        query: Search query text (minimum 1 character)
        tags: Optional filter tags (e.g., ['story'], ['comment'], ['(story,poll)'] for OR logic, ['author_pg'] for author filter)
        numericFilters: Optional numeric filters (e.g., ['points>=100'], ['num_comments>=50'], ['created_at_i>1640000000']). Multiple filters use AND logic.
        page: Page number (0-indexed, default: 0)
        hitsPerPage: Results per page (1-1000, default: 20)
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "tags": tags,
        "numericFilters": numericFilters,
        "page": page,
        "hitsPerPage": hitsPerPage
    }
    
    return call_api("1777316659382275", "search_posts", arguments)

def get_front_page(
    page: Optional[float] = 0.0,
    hitsPerPage: Optional[float] = 30.0
) -> Dict[str, Any]:
    """
    Retrieve posts currently on the HackerNews front page.

Returns stories sorted by HackerNews ranking algorithm. The front page typically contains the most popular and trending stories.

Supports:
- Pagination to view beyond the first page
- Customizable results per page (default: 30)
- All posts are tagged with 'front_page'

Examples:
- Get first page: { }
- Get with custom page size: { "hitsPerPage": 50 }
- Get second page: { "page": 1 }

Returns the same structure as search results with hits, pagination info, and metadata.
    
    Args:
        page: Page number (0-indexed, default: 0)
        hitsPerPage: Results per page (1-1000, default: 30)
    
    Returns:
        
    """
    arguments = {
        "page": page,
        "hitsPerPage": hitsPerPage
    }
    
    return call_api("1777316659382275", "get_front_page", arguments)

def get_latest_posts(
    tags: Optional[null] = None,
    page: Optional[float] = 0.0,
    hitsPerPage: Optional[float] = 20.0
) -> Dict[str, Any]:
    """
    Retrieve the most recent HackerNews posts sorted by date.

Returns posts in chronological order (newest first), including all types of content unless filtered.

Supports:
- Filter by content type using tags (story, comment, poll, show_hn, ask_hn, etc.)
- Pagination to view older posts
- Customizable results per page (default: 20)
- Empty query to get all recent posts

Examples:
- Get latest stories: { "tags": ["story"] }
- Get latest comments: { "tags": ["comment"] }
- Get all recent activity: { }
- Get with custom page size: { "hitsPerPage": 50 }

Use this to monitor real-time HackerNews activity or find the newest content.
    
    Args:
        tags: Optional filter tags (e.g., ['story'], ['comment'])
        page: Page number (0-indexed, default: 0)
        hitsPerPage: Results per page (1-1000, default: 20)
    
    Returns:
        
    """
    arguments = {
        "tags": tags,
        "page": page,
        "hitsPerPage": hitsPerPage
    }
    
    return call_api("1777316659382275", "get_latest_posts", arguments)

def get_item(
    itemId: str
) -> Dict[str, Any]:
    """
    Retrieve detailed information about a specific HackerNews item by ID.

Returns complete item details including the full nested comment tree. Use this to:
- View a story with all comments
- Read a specific comment with its replies
- Explore discussion threads in depth
- Get complete metadata for any item

Features:
- Full nested comment tree (all levels)
- Complete item metadata (title, url, text, points, author, etc.)
- Works for stories, comments, polls, and poll options
- Includes creation time and item type

Examples:
- Get story with comments: { "itemId": "38456789" }
- Get specific comment: { "itemId": "38456790" }
- Get poll: { "itemId": "126809" }

Note: Large comment threads (>500 comments) may take 2-3 seconds to load due to nested fetching.
Returns error if item doesn't exist or has been deleted.
    
    Args:
        itemId: HackerNews item ID (e.g., '38456789')
    
    Returns:
        
    """
    arguments = {
        "itemId": itemId
    }
    
    return call_api("1777316659382275", "get_item", arguments)

def get_user(
    username: str
) -> Dict[str, Any]:
    """
    Retrieve public profile information for a HackerNews user.

Returns user profile including karma, bio, and account creation date. Use this to:
- Check user reputation (karma score)
- Read user bio and about information
- See when account was created
- Verify user existence before searching their content

Features:
- Username (case-sensitive)
- Karma score (total upvotes received)
- About/bio text (may contain HTML)
- Account creation date (Unix timestamp)

Examples:
- Get famous user: { "username": "pg" }
- Check moderator: { "username": "dang" }
- Verify author: { "username": "tptacek" }

Username validation:
- Alphanumeric characters and underscores only
- Case-sensitive
- Must exist on HackerNews

Returns error if user doesn't exist or username format is invalid.
    
    Args:
        username: HackerNews username (alphanumeric + underscores, e.g., 'pg')
    
    Returns:
        
    """
    arguments = {
        "username": username
    }
    
    return call_api("1777316659382275", "get_user", arguments)

