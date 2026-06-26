#!/bin/bash
# IKL Setup Script — creates starter files in workspace/ikl/

set -e

IKL_DIR="${1:-ikl}"

mkdir -p "$IKL_DIR"

# contacts.json
if [ ! -f "$IKL_DIR/contacts.json" ]; then
cat > "$IKL_DIR/contacts.json" << 'EOF'
{
  "contacts": {},
  "relationship_types": [
    "partner", "family", "close_friend", "friend",
    "colleague", "acquaintance", "stranger"
  ],
  "defaults": {
    "unknown_sender": "stranger"
  }
}
EOF
echo "✅ Created $IKL_DIR/contacts.json"
else
  echo "⏭️  $IKL_DIR/contacts.json already exists, skipping"
fi

# permissions.json
if [ ! -f "$IKL_DIR/permissions.json" ]; then
cat > "$IKL_DIR/permissions.json" << 'EOF'
{
  "categories": {
    "personal_facts": {
      "levels": { "1": "Name, nationality", "2": "Birthday, age", "3": "Address, phone" }
    },
    "health": {
      "levels": { "1": "General wellness", "2": "Ongoing conditions", "3": "Diagnoses", "4": "Mental health", "5": "Full history" }
    },
    "schedule": {
      "levels": { "1": "Free/busy", "2": "Event names/times", "3": "Full details" }
    },
    "financial": {
      "levels": { "1": "Employment status", "2": "General comfort", "3": "Salary", "4": "Bank details" }
    },
    "relationships": {
      "levels": { "1": "Status", "2": "Partner name, children", "3": "Dynamics" }
    },
    "location": {
      "levels": { "1": "Country/city", "2": "Neighborhood", "3": "Exact address" }
    },
    "work": {
      "levels": { "1": "Title/company", "2": "Projects", "3": "Internal info" }
    },
    "preferences": {
      "levels": { "1": "Hobbies", "2": "Political/religious", "3": "Deeply personal" }
    }
  },
  "relationship_access": {
    "partner":      { "personal_facts": 3, "health": 5, "schedule": 3, "financial": 4, "relationships": 3, "location": 3, "work": 3, "preferences": 3 },
    "family":       { "personal_facts": 3, "health": 4, "schedule": 3, "financial": 2, "relationships": 3, "location": 2, "work": 2, "preferences": 2 },
    "close_friend": { "personal_facts": 2, "health": 3, "schedule": 3, "financial": 1, "relationships": 2, "location": 2, "work": 2, "preferences": 2 },
    "friend":       { "personal_facts": 2, "health": 1, "schedule": 2, "financial": 1, "relationships": 1, "location": 1, "work": 1, "preferences": 1 },
    "colleague":    { "personal_facts": 1, "health": 1, "schedule": 2, "financial": 1, "relationships": 1, "location": 1, "work": 2, "preferences": 1 },
    "acquaintance": { "personal_facts": 1, "health": 0, "schedule": 1, "financial": 0, "relationships": 0, "location": 1, "work": 1, "preferences": 1 },
    "stranger":     { "personal_facts": 0, "health": 0, "schedule": 0, "financial": 0, "relationships": 0, "location": 0, "work": 0, "preferences": 0 }
  },
  "policy_overrides": {
    "overrides": []
  }
}
EOF
echo "✅ Created $IKL_DIR/permissions.json"
else
  echo "⏭️  $IKL_DIR/permissions.json already exists, skipping"
fi

# knowledge.json
if [ ! -f "$IKL_DIR/knowledge.json" ]; then
cat > "$IKL_DIR/knowledge.json" << 'EOF'
{
  "entries": []
}
EOF
echo "✅ Created $IKL_DIR/knowledge.json"
else
  echo "⏭️  $IKL_DIR/knowledge.json already exists, skipping"
fi

# audit.json
if [ ! -f "$IKL_DIR/audit.json" ]; then
cat > "$IKL_DIR/audit.json" << 'EOF'
{
  "entries": []
}
EOF
echo "✅ Created $IKL_DIR/audit.json"
else
  echo "⏭️  $IKL_DIR/audit.json already exists, skipping"
fi

echo ""
echo "🔐 IKL initialized in $IKL_DIR/"
echo ""
echo "Next steps:"
echo "  1. Add contacts: tell your agent who your contacts are"
echo "  2. Add knowledge: tell your agent what info is OK to store"
echo "  3. Adjust permissions: review defaults in permissions.json"
