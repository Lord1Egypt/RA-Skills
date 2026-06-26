"""
Skill Interface for AI Agents
Provides a standardized interface for AI agents to use Twitter skills.
"""

from typing import Dict, Any, List
from .twitter_skills import TwitterSkills


class TwitterSkillInterface:
    """
    Standardized skill interface for AI agents.
    Each method returns a structured response with metadata.
    """
    
    def __init__(self, auth_token: str = None, rate_limit_delay: float = 1.0):
        """
        Initialize the Twitter Skill Interface.
        
        Args:
            auth_token: Optional Twitter auth_token for authenticated access.
                       If provided, enables access to all features.
                       If not provided, uses guest session (limited features).
            rate_limit_delay: Delay in seconds between requests (default: 1.0).
                            Recommended: 1-2 seconds for normal operations,
                            2-3 seconds for bulk operations.
        """
        self.skills = TwitterSkills(auth_token=auth_token, rate_limit_delay=rate_limit_delay)
        self.available_skills = self._register_skills()
    
    def set_auth_token(self, auth_token: str) -> Dict[str, Any]:
        """
        Set authentication token for accessing restricted features.
        
        Args:
            auth_token: Twitter auth_token for authentication
            
        Returns:
            Dictionary with success status and message
        """
        try:
            self.skills.twitter.generate_session(auth_token=auth_token)
            return {
                "success": True,
                "message": "Authentication successful. Rate limiting is enabled to comply with best practices."
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Authentication failed: {str(e)}"
            }
    
    def _register_skills(self) -> Dict[str, Dict[str, Any]]:
        """Register all available skills with their metadata."""
        return {
            "get_user_profile": {
                "description": "Extract detailed profile information for a Twitter user",
                "parameters": {
                    "username": {
                        "type": "string",
                        "description": "Twitter username without @ symbol",
                        "required": True
                    }
                },
                "returns": "User profile data including bio, followers count, etc."
            },
            "get_user_tweets": {
                "description": "Extract recent tweets from a Twitter user",
                "parameters": {
                    "username": {
                        "type": "string",
                        "description": "Twitter username without @ symbol",
                        "required": True
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of tweets to extract (default: 10)",
                        "required": False,
                        "default": 10
                    }
                },
                "returns": "List of tweets with content, timestamps, and engagement metrics"
            },
            "get_user_followers": {
                "description": "Extract followers list for a Twitter user",
                "parameters": {
                    "username": {
                        "type": "string",
                        "description": "Twitter username without @ symbol",
                        "required": True
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of followers to extract (default: 20)",
                        "required": False,
                        "default": 20
                    }
                },
                "returns": "List of follower profiles"
            },
            "get_user_followings": {
                "description": "Extract following list for a Twitter user",
                "parameters": {
                    "username": {
                        "type": "string",
                        "description": "Twitter username without @ symbol",
                        "required": True
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of followings to extract (default: 20)",
                        "required": False,
                        "default": 20
                    }
                },
                "returns": "List of following profiles"
            },
            "get_user_media": {
                "description": "Extract media (photos/videos) from a Twitter user's tweets",
                "parameters": {
                    "username": {
                        "type": "string",
                        "description": "Twitter username without @ symbol",
                        "required": True
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of media items to extract (default: 10)",
                        "required": False,
                        "default": 10
                    }
                },
                "returns": "List of media URLs and metadata"
            },
            "search_tweets": {
                "description": "Search for tweets matching a query",
                "parameters": {
                    "query": {
                        "type": "string",
                        "description": "Search query string",
                        "required": True
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of tweets to return (default: 10)",
                        "required": False,
                        "default": 10
                    }
                },
                "returns": "List of tweets matching the search query"
            }
        }
    
    def get_available_skills(self) -> Dict[str, Dict[str, Any]]:
        """
        Get list of all available skills with their descriptions.
        AI agents can call this to discover available capabilities.
        """
        return self.available_skills
    
    def execute_skill(self, skill_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a skill by name with given parameters.
        
        Args:
            skill_name: Name of the skill to execute
            parameters: Dictionary of parameters for the skill
            
        Returns:
            Standardized response with success status, data, and metadata
        """
        if skill_name not in self.available_skills:
            return {
                "success": False,
                "error": f"Unknown skill: {skill_name}",
                "available_skills": list(self.available_skills.keys())
            }
        
        try:
            # Route to appropriate skill method
            if skill_name == "get_user_profile":
                result = self.skills.get_user_profile(parameters.get("username"))
            elif skill_name == "get_user_tweets":
                result = self.skills.get_user_tweets(
                    parameters.get("username"),
                    parameters.get("count", 10)
                )
            elif skill_name == "get_user_followers":
                result = self.skills.get_user_followers(
                    parameters.get("username"),
                    parameters.get("count", 20)
                )
            elif skill_name == "get_user_followings":
                result = self.skills.get_user_followings(
                    parameters.get("username"),
                    parameters.get("count", 20)
                )
            elif skill_name == "get_user_media":
                result = self.skills.get_user_media(
                    parameters.get("username"),
                    parameters.get("count", 10)
                )
            elif skill_name == "search_tweets":
                result = self.skills.search_tweets(
                    parameters.get("query"),
                    parameters.get("count", 10)
                )
            else:
                return {
                    "success": False,
                    "error": f"Skill not implemented: {skill_name}"
                }
            
            # Add metadata to response
            result["skill_name"] = skill_name
            result["parameters"] = parameters
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "skill_name": skill_name,
                "parameters": parameters
            }
