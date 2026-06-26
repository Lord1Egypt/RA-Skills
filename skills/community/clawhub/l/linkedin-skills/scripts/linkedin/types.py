"""LinkedIn data type definitions."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Author:
    name: str = ""
    profile_url: str = ""
    headline: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> Author:
        return cls(
            name=d.get("name", ""),
            profile_url=d.get("profileUrl", ""),
            headline=d.get("headline", ""),
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "profileUrl": self.profile_url,
            "headline": self.headline,
        }


@dataclass
class PostStats:
    reactions: int = 0
    comments: int = 0
    reposts: int = 0

    @classmethod
    def from_dict(cls, d: dict) -> PostStats:
        return cls(
            reactions=d.get("reactions", 0),
            comments=d.get("comments", 0),
            reposts=d.get("reposts", 0),
        )

    def to_dict(self) -> dict:
        return {
            "reactions": self.reactions,
            "comments": self.comments,
            "reposts": self.reposts,
        }


@dataclass
class Post:
    urn: str = ""
    url: str = ""
    author: Author = field(default_factory=Author)
    text: str = ""
    post_type: str = ""  # text, image, video, article, share
    created_at: str = ""
    stats: PostStats = field(default_factory=PostStats)

    @classmethod
    def from_dict(cls, d: dict) -> Post:
        return cls(
            urn=d.get("urn", ""),
            url=d.get("url", ""),
            author=Author.from_dict(d.get("author", {})),
            text=d.get("text", ""),
            post_type=d.get("postType", ""),
            created_at=d.get("createdAt", ""),
            stats=PostStats.from_dict(d.get("stats", {})),
        )

    def to_dict(self) -> dict:
        return {
            "urn": self.urn,
            "url": self.url,
            "author": self.author.to_dict(),
            "text": self.text,
            "postType": self.post_type,
            "createdAt": self.created_at,
            "stats": self.stats.to_dict(),
        }


@dataclass
class Comment:
    author: Author = field(default_factory=Author)
    text: str = ""
    created_at: str = ""

    def to_dict(self) -> dict:
        return {
            "author": self.author.to_dict(),
            "text": self.text,
            "createdAt": self.created_at,
        }


@dataclass
class PostDetail:
    post: Post = field(default_factory=Post)
    comments: list[Comment] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            **self.post.to_dict(),
            "comments": [c.to_dict() for c in self.comments],
        }


@dataclass
class Profile:
    name: str = ""
    headline: str = ""
    location: str = ""
    profile_url: str = ""
    connections: str = ""
    about: str = ""
    experience: list[dict] = field(default_factory=list)
    degree: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "headline": self.headline,
            "location": self.location,
            "profileUrl": self.profile_url,
            "connections": self.connections,
            "about": self.about,
            "experience": self.experience,
            "degree": self.degree,
        }


@dataclass
class CompanyProfile:
    name: str = ""
    tagline: str = ""
    followers: str = ""
    about: str = ""
    website: str = ""
    company_url: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "tagline": self.tagline,
            "followers": self.followers,
            "about": self.about,
            "website": self.website,
            "companyUrl": self.company_url,
        }


@dataclass
class SearchResult:
    name: str = ""
    subtitle: str = ""
    url: str = ""
    result_type: str = ""  # person, company, post
    degree: str = ""       # 1st, 2nd, 3rd (people only)
    location: str = ""     # location text (people only)

    def to_dict(self) -> dict:
        d = {
            "name": self.name,
            "subtitle": self.subtitle,
            "url": self.url,
            "resultType": self.result_type,
        }
        if self.degree:
            d["degree"] = self.degree
        if self.location:
            d["location"] = self.location
        return d


@dataclass
class ActionResult:
    success: bool = False
    message: str = ""
    url: str = ""

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "message": self.message,
            "url": self.url,
        }


@dataclass
class SubmitPostContent:
    text: str = ""
    images: list[str] = field(default_factory=list)
