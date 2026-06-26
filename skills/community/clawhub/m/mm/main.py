class MemoryManager:
    def __init__(self):
        self.memories = {}
        self.reminders = []
        self.connections = {}
    
    def save_memory(self, content, tags=None):
        """Save a new memory"""
        memory_id = len(self.memories) + 1
        self.memories[memory_id] = {
            'content': content,
            'tags': tags or [],
            'timestamp': self._get_current_time()
        }
        return f"Memory saved with ID: {memory_id}"
    
    def set_reminder(self, content, time, location=None):
        """Set a reminder"""
        reminder_id = len(self.reminders) + 1
        self.reminders.append({
            'id': reminder_id,
            'content': content,
            'time': time,
            'location': location,
            'status': 'pending'
        })
        return f"Reminder set with ID: {reminder_id}"
    
    def link_memories(self, memory_id1, memory_id2):
        """Link two memories"""
        if memory_id1 not in self.memories or memory_id2 not in self.memories:
            return "Error: One or both memory IDs do not exist"
        
        if memory_id1 not in self.connections:
            self.connections[memory_id1] = []
        if memory_id2 not in self.connections:
            self.connections[memory_id2] = []
        
        self.connections[memory_id1].append(memory_id2)
        self.connections[memory_id2].append(memory_id1)
        
        return f"Memories {memory_id1} and {memory_id2} linked successfully"
    
    def search_memories(self, query):
        """Search memories by query"""
        results = []
        for memory_id, memory in self.memories.items():
            if query.lower() in memory['content'].lower():
                results.append((memory_id, memory['content']))
        
        if not results:
            return "No memories found matching your query"
        
        response = "Found memories:\n"
        for memory_id, content in results:
            response += f"ID {memory_id}: {content}\n"
        return response
    
    def list_reminders(self):
        """List all pending reminders"""
        pending_reminders = [r for r in self.reminders if r['status'] == 'pending']
        
        if not pending_reminders:
            return "No pending reminders"
        
        response = "Pending reminders:\n"
        for reminder in pending_reminders:
            location_info = f" at {reminder['location']}" if reminder['location'] else ""
            response += f"ID {reminder['id']}: {reminder['content']} (Time: {reminder['time']}{location_info})\n"
        return response
    
    def _get_current_time(self):
        """Get current time as string"""
        import datetime
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Main function to handle skill requests
def handle_request(request):
    mm = MemoryManager()
    
    # Example request handling
    if "remember" in request.lower():
        content = request.lower().replace("remember", "").strip()
        return mm.save_memory(content)
    elif "remind" in request.lower():
        # Simple parsing for demonstration
        content = request.lower().replace("remind me", "").strip()
        return mm.set_reminder(content, "2023-12-31 23:59:59")
    elif "link" in request.lower():
        # Simple parsing for demonstration
        return mm.link_memories(1, 2)
    elif "search" in request.lower() or "what did i save" in request.lower():
        query = request.lower().replace("search", "").replace("what did i save about", "").strip()
        return mm.search_memories(query)
    elif "reminders" in request.lower():
        return mm.list_reminders()
    else:
        return "I can help you manage your memories. You can ask me to remember something, set a reminder, link memories, search for saved information, or list your reminders."

# Test the skill
if __name__ == "__main__":
    test_requests = [
        "Remember that my anniversary is on June 15th",
        "Remind me to buy milk",
        "Search for anniversary",
        "List my reminders"
    ]
    
    for req in test_requests:
        print(f"Request: {req}")
        print(f"Response: {handle_request(req)}")
        print()
