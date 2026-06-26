#!/bin/bash
# Preny Analytics - Conversations Script
# Usage: 
#   ./preny-conversations.sh list [pending|processing|closed]
#   ./preny-conversations.sh get <conversation_id>
#   ./preny-conversations.sh reply <conversation_id> <message>

set -e

API_URL="${PRENY_API_URL:-https://api.preny.ai/v1}"
API_KEY="${PRENY_API_KEY}"
WORKSPACE_ID="${PRENY_WORKSPACE_ID}"

if [ -z "$API_KEY" ] || [ -z "$WORKSPACE_ID" ]; then
    echo "Error: Missing PRENY_API_KEY or PRENY_WORKSPACE_ID"
    exit 1
fi

ACTION="${1:-list}"
shift || true

case "$ACTION" in
    list)
        STATUS="${1:-all}"
        echo "📋 DANH SÁCH HỘI THOẠI (Status: $STATUS)"
        echo ""
        
        response=$(curl -s -X GET \
            "${API_URL}/conversations?status=${STATUS}&limit=20" \
            -H "Authorization: Bearer ${API_KEY}" \
            -H "X-Workspace-ID: ${WORKSPACE_ID}" \
            -H "Content-Type: application/json")
        
        echo "$response" | jq -r '.data.conversations[] | 
            "ID: \(.id) | \(.customerName) | \(.channel) | \(.status) | Chưa đọc: \(.unreadCount) | \(.lastMessage[:50])..."'
        ;;
    
    get)
        CONV_ID="$1"
        if [ -z "$CONV_ID" ]; then
            echo "Error: Missing conversation ID"
            exit 1
        fi
        
        echo "📂 CHI TIẾT HỘI THOẠI: $CONV_ID"
        echo ""
        
        response=$(curl -s -X GET \
            "${API_URL}/conversations/${CONV_ID}" \
            -H "Authorization: Bearer ${API_KEY}" \
            -H "X-Workspace-ID: ${WORKSPACE_ID}" \
            -H "Content-Type: application/json")
        
        echo "┌─────────────────────────────────────────┐"
        echo "│ 👤 Khách hàng: $(echo "$response" | jq -r '.data.customer.name')"
        echo "│ 📞 SĐT:        $(echo "$response" | jq -r '.data.customer.phone')"
        echo "│ 📧 Email:      $(echo "$response" | jq -r '.data.customer.email')"
        echo "│ 📱 Kênh:       $(echo "$response" | jq -r '.data.channel')"
        echo "│ 🏷️  Trạng thái: $(echo "$response" | jq -r '.data.status')"
        echo "└─────────────────────────────────────────┘"
        echo ""
        echo "💬 TIN NHẮN:"
        echo "───────────────────────────────────────────"
        echo "$response" | jq -r '.data.messages[] | "[\(.timestamp)] \(.sender): \(.content)"'
        ;;
    
    reply)
        CONV_ID="$1"
        MESSAGE="$2"
        
        if [ -z "$CONV_ID" ] || [ -z "$MESSAGE" ]; then
            echo "Error: Missing conversation ID or message"
            echo "Usage: ./preny-conversations.sh reply <conv_id> <message>"
            exit 1
        fi
        
        # ⚠️ ASK BEFORE SENDING
        echo "⚠️  Bạn có muốn gửi tin nhắn sau không?"
        echo ""
        echo "Hội thoại: $CONV_ID"
        echo "Nội dung: $MESSAGE"
        echo ""
        read -p "Xác nhận gửi? (y/N): " confirm
        
        if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
            echo "❌ Đã hủy gửi tin nhắn"
            exit 0
        fi
        
        response=$(curl -s -X POST \
            "${API_URL}/conversations/${CONV_ID}/messages" \
            -H "Authorization: Bearer ${API_KEY}" \
            -H "X-Workspace-ID: ${WORKSPACE_ID}" \
            -H "Content-Type: application/json" \
            -d "{\"type\":\"text\",\"content\":\"${MESSAGE}\",\"sender\":\"agent\"}")
        
        if echo "$response" | jq -e '.success == true' > /dev/null 2>&1; then
            echo "✅ Đã gửi tin nhắn thành công!"
            echo "Message ID: $(echo "$response" | jq -r '.data.messageId')"
        else
            echo "❌ Lỗi: $(echo "$response" | jq -r '.error.message')"
        fi
        ;;
    
    *)
        echo "Unknown action: $ACTION"
        echo "Usage:"
        echo "  ./preny-conversations.sh list [pending|processing|closed]"
        echo "  ./preny-conversations.sh get <conversation_id>"
        echo "  ./preny-conversations.sh reply <conversation_id> <message>"
        exit 1
        ;;
esac
