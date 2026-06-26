#!/usr/bin/env python3
"""
KnowledgeKeeper Skill - Knowledge management and information organization tool
"""

import json
import os
import time

class KnowledgeKeeper:
    def __init__(self):
        self.notes_file = "knowledge.json"
        self.load_notes()
    
    def load_notes(self):
        """Load notes from file"""
        if os.path.exists(self.notes_file):
            with open(self.notes_file, 'r', encoding='utf-8') as f:
                self.notes = json.load(f)
        else:
            self.notes = {
                "categories": {},
                "tags": {},
                "notes": []
            }
    
    def save_notes(self):
        """Save notes to file"""
        with open(self.notes_file, 'w', encoding='utf-8') as f:
            json.dump(self.notes, f, indent=2, ensure_ascii=False)
    
    def add_note(self, title, content, category=None, tags=None):
        """Add a new note"""
        note_id = f"note_{int(time.time())}"
        note = {
            "id": note_id,
            "title": title,
            "content": content,
            "category": category,
            "tags": tags or [],
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.notes["notes"].append(note)
        
        # Update categories
        if category:
            if category not in self.notes["categories"]:
                self.notes["categories"][category] = []
            self.notes["categories"][category].append(note_id)
        
        # Update tags
        for tag in tags or []:
            if tag not in self.notes["tags"]:
                self.notes["tags"][tag] = []
            self.notes["tags"][tag].append(note_id)
        
        self.save_notes()
        return f"Note '{title}' added successfully"
    
    def search_notes(self, query):
        """Search notes by query"""
        results = []
        for note in self.notes["notes"]:
            if query.lower() in note["title"].lower() or query.lower() in note["content"].lower():
                results.append(note)
        return results
    
    def list_notes(self, category=None, tag=None):
        """List notes by category or tag"""
        if category:
            if category in self.notes["categories"]:
                note_ids = self.notes["categories"][category]
                return [note for note in self.notes["notes"] if note["id"] in note_ids]
            else:
                return f"No notes found in category: {category}"
        elif tag:
            if tag in self.notes["tags"]:
                note_ids = self.notes["tags"][tag]
                return [note for note in self.notes["notes"] if note["id"] in note_ids]
            else:
                return f"No notes found with tag: {tag}"
        else:
            return self.notes["notes"]
    
    def update_note(self, note_id, title=None, content=None, category=None, tags=None):
        """Update an existing note"""
        for note in self.notes["notes"]:
            if note["id"] == note_id:
                if title:
                    note["title"] = title
                if content:
                    note["content"] = content
                if category:
                    # Remove from old category
                    if note["category"] and note["category"] in self.notes["categories"]:
                        if note_id in self.notes["categories"][note["category"]]:
                            self.notes["categories"][note["category"]].remove(note_id)
                    # Add to new category
                    if category not in self.notes["categories"]:
                        self.notes["categories"][category] = []
                    self.notes["categories"][category].append(note_id)
                    note["category"] = category
                if tags is not None:
                    # Remove from old tags
                    for old_tag in note["tags"]:
                        if old_tag in self.notes["tags"] and note_id in self.notes["tags"][old_tag]:
                            self.notes["tags"][old_tag].remove(note_id)
                    # Add to new tags
                    note["tags"] = tags
                    for new_tag in tags:
                        if new_tag not in self.notes["tags"]:
                            self.notes["tags"][new_tag] = []
                        self.notes["tags"][new_tag].append(note_id)
                note["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                self.save_notes()
                return f"Note updated successfully"
        return f"Note with id {note_id} not found"
    
    def export_notes(self, format="json"):
        """Export notes in different formats"""
        if format == "json":
            return json.dumps(self.notes, indent=2, ensure_ascii=False)
        elif format == "markdown":
            markdown = "# KnowledgeKeeper Notes\n\n"
            for note in self.notes["notes"]:
                markdown += f"## {note['title']}\n"
                markdown += f"*Created: {note['created_at']}*\n"
                if note['category']:
                    markdown += f"*Category: {note['category']}*\n"
                if note['tags']:
                    markdown += f"*Tags: {', '.join(note['tags'])}*\n"
                markdown += "\n"
                markdown += f"{note['content']}\n"
                markdown += "\n" + "-"*40 + "\n\n"
            return markdown
        else:
            return "Unsupported export format"

def handler(event):
    """Handle skill activation"""
    keeper = KnowledgeKeeper()
    
    # Parse the event to determine the action
    if "action" in event:
        action = event["action"]
        
        if action == "add_note":
            title = event.get("title")
            content = event.get("content")
            category = event.get("category")
            tags = event.get("tags")
            return keeper.add_note(title, content, category, tags)
        
        elif action == "search_notes":
            query = event.get("query")
            return keeper.search_notes(query)
        
        elif action == "list_notes":
            category = event.get("category")
            tag = event.get("tag")
            return keeper.list_notes(category, tag)
        
        elif action == "update_note":
            note_id = event.get("id")
            title = event.get("title")
            content = event.get("content")
            category = event.get("category")
            tags = event.get("tags")
            return keeper.update_note(note_id, title, content, category, tags)
        
        elif action == "export_notes":
            format = event.get("format", "json")
            return keeper.export_notes(format)
        
        else:
            return "Unknown action"
    
    return "KnowledgeKeeper skill activated. Use 'add_note', 'search_notes', 'list_notes', 'update_note', or 'export_notes' actions."

if __name__ == "__main__":
    # Test the skill
    test_event = {"action": "add_note", "title": "Test Note", "content": "This is a test note", "category": "Testing", "tags": ["test", "example"]}
    print(handler(test_event))

