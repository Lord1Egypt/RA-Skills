"""
Template Registry: Store, retrieve, and manage query templates.

Provides persistent storage and caching for query templates,
supporting search, versioning, and template organization.

Author: Knowledge Graph Project
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
import json


# ============================================================================
# Template Registry
# ============================================================================

@dataclass
class TemplateVersion:
    """Version information for a template."""
    version: str
    created_at: str
    created_by: str
    changes: str
    is_current: bool = False


@dataclass
class TemplateMetadata:
    """Metadata for a template."""
    template_id: str
    created_at: str
    updated_at: str
    author: str
    category: str
    tags: List[str] = field(default_factory=list)
    usage_count: int = 0
    rating: float = 0.0
    versions: List[TemplateVersion] = field(default_factory=list)
    related_templates: List[str] = field(default_factory=list)


class TemplateRegistry:
    """Manages template storage and retrieval."""
    
    def __init__(self):
        """Initialize template registry."""
        self.templates: Dict[str, Dict[str, Any]] = {}
        self.metadata: Dict[str, TemplateMetadata] = {}
        self.index: Dict[str, List[str]] = {
            "tags": {},
            "category": {},
            "language": {}
        }
    
    def register_template(
        self,
        template_id: str,
        template_data: Dict[str, Any],
        category: str = "general",
        tags: Optional[List[str]] = None,
        author: str = "system"
    ):
        """Register a new template."""
        self.templates[template_id] = template_data
        
        metadata = TemplateMetadata(
            template_id=template_id,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            author=author,
            category=category,
            tags=tags or []
        )
        self.metadata[template_id] = metadata
        
        # Update indexes
        self._update_indexes(template_id, metadata)
    
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a template."""
        if template_id in self.templates:
            # Update usage count
            self.metadata[template_id].usage_count += 1
            return self.templates[template_id]
        return None
    
    def search_templates(
        self,
        query: str = "",
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        language: Optional[str] = None
    ) -> List[str]:
        """Search templates by criteria."""
        results = list(self.templates.keys())
        
        # Filter by category
        if category:
            results = [
                t for t in results
                if self.metadata[t].category == category
            ]
        
        # Filter by language
        if language:
            results = [
                t for t in results
                if self.templates[t].get("language") == language
            ]
        
        # Filter by tags
        if tags:
            results = [
                t for t in results
                if any(tag in self.metadata[t].tags for tag in tags)
            ]
        
        # Filter by query string (name/description)
        if query:
            results = [
                t for t in results
                if query.lower() in t.lower() or
                   query.lower() in self.templates[t].get("description", "").lower()
            ]
        
        return results
    
    def get_category_templates(self, category: str) -> List[str]:
        """Get all templates in a category."""
        return [
            t for t in self.templates.keys()
            if self.metadata[t].category == category
        ]
    
    def get_templates_by_tag(self, tag: str) -> List[str]:
        """Get templates with a specific tag."""
        return self.index["tags"].get(tag, [])
    
    def get_popular_templates(self, limit: int = 10) -> List[str]:
        """Get most-used templates."""
        sorted_templates = sorted(
            self.metadata.items(),
            key=lambda x: x[1].usage_count,
            reverse=True
        )
        return [t[0] for t in sorted_templates[:limit]]
    
    def get_highest_rated(self, limit: int = 10) -> List[str]:
        """Get highest-rated templates."""
        sorted_templates = sorted(
            self.metadata.items(),
            key=lambda x: x[1].rating,
            reverse=True
        )
        return [t[0] for t in sorted_templates[:limit]]
    
    def rate_template(self, template_id: str, rating: float):
        """Rate a template (0-5 stars)."""
        if template_id in self.metadata:
            # Simple average - in production, track individual ratings
            current_rating = self.metadata[template_id].rating
            usage = self.metadata[template_id].usage_count
            new_rating = (current_rating * usage + rating) / (usage + 1)
            self.metadata[template_id].rating = min(5.0, max(0.0, new_rating))
    
    def add_tag(self, template_id: str, tag: str):
        """Add a tag to a template."""
        if template_id in self.metadata:
            if tag not in self.metadata[template_id].tags:
                self.metadata[template_id].tags.append(tag)
                self._update_tag_index(template_id, tag)
    
    def remove_tag(self, template_id: str, tag: str):
        """Remove a tag from a template."""
        if template_id in self.metadata:
            if tag in self.metadata[template_id].tags:
                self.metadata[template_id].tags.remove(tag)
    
    def create_version(
        self,
        template_id: str,
        version: str,
        changes: str,
        created_by: str = "system"
    ):
        """Create a new version of a template."""
        if template_id not in self.metadata:
            return
        
        # Mark current version as not current
        for v in self.metadata[template_id].versions:
            v.is_current = False
        
        # Add new version
        new_version = TemplateVersion(
            version=version,
            created_at=datetime.now().isoformat(),
            created_by=created_by,
            changes=changes,
            is_current=True
        )
        self.metadata[template_id].versions.append(new_version)
        self.metadata[template_id].updated_at = datetime.now().isoformat()
    
    def update_template(
        self,
        template_id: str,
        new_template_data: Dict[str, Any],
        version: str = "1.0.1",
        changes: str = "Update",
        updated_by: str = "system"
    ):
        """Update an existing template."""
        if template_id not in self.templates:
            return
        
        self.templates[template_id].update(new_template_data)
        self.create_version(template_id, version, changes, updated_by)
    
    def get_related_templates(self, template_id: str) -> List[str]:
        """Get related templates."""
        if template_id not in self.metadata:
            return []
        return self.metadata[template_id].related_templates
    
    def add_related(self, template_id: str, related_id: str):
        """Add a related template."""
        if template_id in self.metadata:
            if related_id not in self.metadata[template_id].related_templates:
                self.metadata[template_id].related_templates.append(related_id)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        languages = {}
        categories = {}
        total_usage = 0
        avg_rating = 0.0
        
        for meta in self.metadata.values():
            category = meta.category
            lang = "unknown"
            
            if meta.template_id in self.templates:
                lang = self.templates[meta.template_id].get("language", "unknown")
            
            languages[lang] = languages.get(lang, 0) + 1
            categories[category] = categories.get(category, 0) + 1
            total_usage += meta.usage_count
            avg_rating += meta.rating
        
        if self.metadata:
            avg_rating /= len(self.metadata)
        
        return {
            "total_templates": len(self.templates),
            "languages": languages,
            "categories": categories,
            "total_usage": total_usage,
            "average_rating": avg_rating,
            "template_count_by_category": categories
        }
    
    def export_templates(self, category: Optional[str] = None) -> str:
        """Export templates to JSON."""
        templates_to_export = {}
        
        if category:
            template_ids = self.get_category_templates(category)
        else:
            template_ids = list(self.templates.keys())
        
        for t_id in template_ids:
            templates_to_export[t_id] = {
                "template": self.templates[t_id],
                "metadata": {
                    "created_at": self.metadata[t_id].created_at,
                    "updated_at": self.metadata[t_id].updated_at,
                    "author": self.metadata[t_id].author,
                    "category": self.metadata[t_id].category,
                    "tags": self.metadata[t_id].tags,
                    "usage_count": self.metadata[t_id].usage_count,
                    "rating": self.metadata[t_id].rating
                }
            }
        
        return json.dumps(templates_to_export, indent=2)
    
    def import_templates(self, json_data: str):
        """Import templates from JSON."""
        templates_data = json.loads(json_data)
        
        for template_id, data in templates_data.items():
            template = data.get("template", {})
            meta = data.get("metadata", {})
            
            self.templates[template_id] = template
            
            metadata = TemplateMetadata(
                template_id=template_id,
                created_at=meta.get("created_at", datetime.now().isoformat()),
                updated_at=meta.get("updated_at", datetime.now().isoformat()),
                author=meta.get("author", "imported"),
                category=meta.get("category", "general"),
                tags=meta.get("tags", []),
                usage_count=meta.get("usage_count", 0),
                rating=meta.get("rating", 0.0)
            )
            self.metadata[template_id] = metadata
            self._update_indexes(template_id, metadata)
    
    def _update_indexes(self, template_id: str, metadata: TemplateMetadata):
        """Update indexes for a template."""
        # Update language index
        if template_id in self.templates:
            lang = self.templates[template_id].get("language")
            if lang not in self.index["language"]:
                self.index["language"][lang] = []
            if template_id not in self.index["language"][lang]:
                self.index["language"][lang].append(template_id)
        
        # Update category index
        category = metadata.category
        if category not in self.index["category"]:
            self.index["category"][category] = []
        if template_id not in self.index["category"][category]:
            self.index["category"][category].append(template_id)
        
        # Update tag indexes
        for tag in metadata.tags:
            self._update_tag_index(template_id, tag)
    
    def _update_tag_index(self, template_id: str, tag: str):
        """Update tag index."""
        if tag not in self.index["tags"]:
            self.index["tags"][tag] = []
        if template_id not in self.index["tags"][tag]:
            self.index["tags"][tag].append(template_id)
    
    def print_stats(self):
        """Print registry statistics."""
        stats = self.get_stats()
        print("\n" + "="*50)
        print("Template Registry Statistics")
        print("="*50)
        print(f"Total Templates: {stats['total_templates']}")
        print(f"Total Usage: {stats['total_usage']}")
        print(f"Average Rating: {stats['average_rating']:.2f}/5.0")
        print(f"\nBy Language:")
        for lang, count in stats['languages'].items():
            print(f"  - {lang}: {count}")
        print(f"\nBy Category:")
        for cat, count in stats['template_count_by_category'].items():
            print(f"  - {cat}: {count}")
        print("="*50 + "\n")


# ============================================================================
# Usage Example
# ============================================================================

if __name__ == "__main__":
    print("🚀 Template Registry - Example Usage\n")
    
    registry = TemplateRegistry()
    
    # Register some templates
    registry.register_template(
        "find_person",
        {
            "language": "cypher",
            "query": "MATCH (p:Person {email: $email}) RETURN p",
            "description": "Find person by email"
        },
        category="search",
        tags=["person", "email", "lookup"],
        author="admin"
    )
    
    registry.register_template(
        "find_relationships",
        {
            "language": "cypher",
            "query": "MATCH (a:$label1)-[:$rel]->(b:$label2) RETURN a, b",
            "description": "Find relationships between nodes"
        },
        category="traversal",
        tags=["relationships", "cypher"],
        author="admin"
    )
    
    # Rate templates
    registry.rate_template("find_person", 5.0)
    registry.rate_template("find_relationships", 4.5)
    
    # Search templates
    print("Templates with 'person' tag:")
    for t_id in registry.get_templates_by_tag("person"):
        print(f"  - {t_id}")
    
    # Get statistics
    registry.print_stats()
    
    print("✅ Template Registry Ready!")
