"""
Twitter Skills Module
Provides skills for extracting Twitter data using tweeterpy.
"""

from typing import List, Dict, Optional, Any
from tweeterpy import TweeterPy
import time


class TwitterSkills:
    """
    A class that provides various Twitter data extraction skills.
    Includes built-in rate limiting to comply with best practices.
    """
    
    def __init__(self, auth_token=None, rate_limit_delay=1.0):
        """
        Initialize Twitter API wrapper
        
        Args:
            auth_token (str, optional): Twitter auth token for authenticated requests.
                                       If None, will try to create guest session.
            rate_limit_delay (float, optional): Delay in seconds between requests (default: 1.0).
                                               Recommended: 1-2 seconds for normal operations,
                                               2-3 seconds for bulk operations.
        """
        self.rate_limit_delay = rate_limit_delay
        self.last_request_time = 0
        if auth_token:
            # Initialize with auth token
            try:
                self.twitter = TweeterPy()
                self.twitter.generate_session(auth_token=auth_token)
            except Exception as e:
                print(f"Warning: Failed to initialize with auth token: {e}")
                print("Falling back to guest session...")
                try:
                    self.twitter = TweeterPy()
                except Exception as e2:
                    print(f"Error: Failed to create guest session: {e2}")
                    raise
        else:
            # Try to create guest session
            try:
                self.twitter = TweeterPy()
            except Exception as e:
                print(f"Warning: Failed to create guest session: {e}")
                print("Some features may not work without authentication.")
                raise
    
    def _apply_rate_limit(self):
        """Apply rate limiting delay between requests."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last_request
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def get_user_profile(self, username: str) -> Dict[str, Any]:
        """
        Extract user profile details.
        
        Args:
            username: Twitter username (without @)
            
        Returns:
            Dictionary containing user profile information
        """
        self._apply_rate_limit()
        try:
            user_data = self.twitter.get_user_data(username)
            return {
                "success": True,
                "data": user_data
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_user_tweets(self, username: str, count: int = 10) -> Dict[str, Any]:
        """
        Extract user's tweets.
        
        Args:
            username: Twitter username (without @)
            count: Number of tweets to extract (default: 10)
            
        Returns:
            Dictionary containing tweets data
        """
        self._apply_rate_limit()
        try:
            # First get user_id from username
            user_id = self.twitter.get_user_id(username)
            # Then get tweets using user_id
            result = self.twitter.get_user_tweets(user_id, total=count)
            return {
                "success": True,
                "data": result.get('data', []),
                "count": len(result.get('data', [])),
                "has_next_page": result.get('has_next_page', False),
                "cursor": result.get('cursor_endpoint')
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_user_followers(self, username: str, count: int = 20) -> Dict[str, Any]:
        """
        Extract user's followers. (LOGIN REQUIRED)
        
        Args:
            username: Twitter username (without @)
            count: Number of followers to extract (default: 20)
            
        Returns:
            Dictionary containing followers data
        """
        self._apply_rate_limit()
        try:
            # First get user_id from username
            user_id = self.twitter.get_user_id(username)
            # Then get followers using user_id with follower=True
            result = self.twitter.get_friends(user_id, follower=True, total=count)
            return {
                "success": True,
                "data": result.get('data', []),
                "count": len(result.get('data', [])),
                "has_next_page": result.get('has_next_page', False),
                "cursor": result.get('cursor_endpoint')
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_user_followings(self, username: str, count: int = 20) -> Dict[str, Any]:
        """
        Extract user's followings. (LOGIN REQUIRED)
        
        Args:
            username: Twitter username (without @)
            count: Number of followings to extract (default: 20)
            
        Returns:
            Dictionary containing followings data
        """
        self._apply_rate_limit()
        try:
            # First get user_id from username
            user_id = self.twitter.get_user_id(username)
            # Then get followings using user_id with following=True
            result = self.twitter.get_friends(user_id, following=True, total=count)
            return {
                "success": True,
                "data": result.get('data', []),
                "count": len(result.get('data', [])),
                "has_next_page": result.get('has_next_page', False),
                "cursor": result.get('cursor_endpoint')
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_user_media(self, username: str, count: int = 10) -> Dict[str, Any]:
        """
        Extract user's media (photos/videos). (LOGIN REQUIRED)
        
        Args:
            username: Twitter username (without @)
            count: Number of media items to extract (default: 10)
            
        Returns:
            Dictionary containing media data
        """
        self._apply_rate_limit()
        try:
            # First get user_id from username
            user_id = self.twitter.get_user_id(username)
            # Then get media using user_id
            result = self.twitter.get_user_media(user_id, total=count)
            return {
                "success": True,
                "data": result.get('data', []),
                "count": len(result.get('data', [])),
                "has_next_page": result.get('has_next_page', False),
                "cursor": result.get('cursor_endpoint')
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def search_tweets(self, query: str, count: int = 10, search_filter: str = "Top") -> Dict[str, Any]:
        """
        Search for tweets by query. (LOGIN REQUIRED)
        
        Args:
            query: Search query string
            count: Number of tweets to return (default: 10)
            search_filter: Type of search - Latest, Top, People, Photos, Videos (default: Top)
            
        Returns:
            Dictionary containing search results
        """
        self._apply_rate_limit()
        try:
            result = self.twitter.search(query, total=count, search_filter=search_filter)
            return {
                "success": True,
                "data": result.get('data', []),
                "count": len(result.get('data', [])),
                "has_next_page": result.get('has_next_page', False),
                "cursor": result.get('cursor_endpoint')
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
