"""
Invoice Forge - Client Management
Manage client database for invoice generation.

Author: Shadow Rose
License: MIT
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class ClientManager:
    """Manage client database stored as JSONL."""
    
    def __init__(self, clients_file: str = "data/clients.jsonl"):
        self.clients_file = clients_file
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist."""
        dirname = os.path.dirname(self.clients_file)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)
    
    def add_client(self, client_id: str, name: str, email: str, 
                   address: str = "", phone: str = "", 
                   notes: str = "", **extra_fields) -> Dict:
        """
        Add a new client to the database.
        
        Args:
            client_id: Unique identifier for client
            name: Client name or company name
            email: Client email
            address: Client address (optional)
            phone: Client phone (optional)
            notes: Additional notes (optional)
            **extra_fields: Any additional fields to store
        
        Returns:
            Client record dictionary
        """
        # Check if client exists
        existing = self.get_client(client_id)
        if existing:
            raise ValueError(f"Client {client_id} already exists. Use update_client() to modify.")
        
        client = {
            "client_id": client_id,
            "name": name,
            "email": email,
            "address": address,
            "phone": phone,
            "notes": notes,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            **extra_fields
        }
        
        # Append to JSONL
        with open(self.clients_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(client) + "\n")
        
        return client
    
    def get_client(self, client_id: str) -> Optional[Dict]:
        """
        Get client by ID.
        
        Args:
            client_id: Client identifier
        
        Returns:
            Client dictionary or None if not found
        """
        if not os.path.exists(self.clients_file):
            return None
        
        with open(self.clients_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    client = json.loads(line)
                    if client.get("client_id") == client_id:
                        return client
        
        return None
    
    def update_client(self, client_id: str, **updates) -> Optional[Dict]:
        """
        Update an existing client.
        
        Args:
            client_id: Client identifier
            **updates: Fields to update
        
        Returns:
            Updated client dictionary or None if not found
        """
        clients = self.list_clients()
        updated = False
        
        for client in clients:
            if client.get("client_id") == client_id:
                client.update(updates)
                client["updated_at"] = datetime.now().isoformat()
                updated = True
                break
        
        if not updated:
            return None
        
        # Rewrite entire file
        self._write_all_clients(clients)
        
        return self.get_client(client_id)
    
    def delete_client(self, client_id: str) -> bool:
        """
        Delete a client from the database.
        
        Args:
            client_id: Client identifier
        
        Returns:
            True if deleted, False if not found
        """
        clients = self.list_clients()
        original_count = len(clients)
        
        clients = [c for c in clients if c.get("client_id") != client_id]
        
        if len(clients) == original_count:
            return False  # Client not found
        
        self._write_all_clients(clients)
        return True
    
    def list_clients(self, search: str = "") -> List[Dict]:
        """
        List all clients, optionally filtered by search term.
        
        Args:
            search: Search term (matches name, email, client_id)
        
        Returns:
            List of client dictionaries
        """
        if not os.path.exists(self.clients_file):
            return []
        
        clients = []
        with open(self.clients_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    client = json.loads(line)
                    clients.append(client)
        
        if search:
            search_lower = search.lower()
            clients = [
                c for c in clients
                if search_lower in c.get("name", "").lower()
                or search_lower in c.get("email", "").lower()
                or search_lower in c.get("client_id", "").lower()
            ]
        
        return sorted(clients, key=lambda c: c.get("name", ""))
    
    def _write_all_clients(self, clients: List[Dict]):
        """Rewrite the entire clients file."""
        with open(self.clients_file, "w", encoding="utf-8") as f:
            for client in clients:
                f.write(json.dumps(client) + "\n")


def main():
    """CLI for client management."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python invoice_clients.py add <id> <name> <email> [address] [phone]")
        print("  python invoice_clients.py get <id>")
        print("  python invoice_clients.py list [search_term]")
        print("  python invoice_clients.py update <id> <field=value> [field=value...]")
        print("  python invoice_clients.py delete <id>")
        sys.exit(1)
    
    manager = ClientManager()
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 5:
            print("Error: add requires <id> <name> <email>")
            sys.exit(1)
        
        client_id = sys.argv[2]
        name = sys.argv[3]
        email = sys.argv[4]
        address = sys.argv[5] if len(sys.argv) > 5 else ""
        phone = sys.argv[6] if len(sys.argv) > 6 else ""
        
        try:
            client = manager.add_client(client_id, name, email, address, phone)
            print(f"✓ Client added: {client['name']} ({client_id})")
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    elif command == "get":
        if len(sys.argv) < 3:
            print("Error: get requires <id>")
            sys.exit(1)
        
        client = manager.get_client(sys.argv[2])
        if client:
            print(json.dumps(client, indent=2))
        else:
            print(f"Client not found: {sys.argv[2]}")
            sys.exit(1)
    
    elif command == "list":
        search = sys.argv[2] if len(sys.argv) > 2 else ""
        clients = manager.list_clients(search)
        
        if not clients:
            print("No clients found.")
        else:
            print(f"{'ID':<20} {'Name':<30} {'Email':<30}")
            print("-" * 80)
            for client in clients:
                print(f"{client['client_id']:<20} {client['name']:<30} {client['email']:<30}")
    
    elif command == "update":
        if len(sys.argv) < 4:
            print("Error: update requires <id> <field=value> [field=value...]")
            sys.exit(1)
        
        client_id = sys.argv[2]
        updates = {}
        
        for arg in sys.argv[3:]:
            if "=" not in arg:
                print(f"Error: Invalid update format: {arg}")
                print("Use field=value format")
                sys.exit(1)
            
            field, value = arg.split("=", 1)
            updates[field] = value
        
        client = manager.update_client(client_id, **updates)
        if client:
            print(f"✓ Client updated: {client['name']}")
        else:
            print(f"Client not found: {client_id}")
            sys.exit(1)
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: delete requires <id>")
            sys.exit(1)
        
        if manager.delete_client(sys.argv[2]):
            print(f"✓ Client deleted: {sys.argv[2]}")
        else:
            print(f"Client not found: {sys.argv[2]}")
            sys.exit(1)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
