Outlook (via Maton Gateway)

Access the Microsoft Outlook API (via Microsoft Graph) with managed OAuth authentication. Read, send, and manage emails, folders, calendar events, and contacts.

🚀 Quick Start
Get User Profile
curl https://gateway.maton.ai/outlook/v1.0/me \
  -H "Authorization: Bearer $MATON_API_KEY" | jq

🌐 Base URL
https://gateway.maton.ai/outlook/{native-api-path}


Example:

/outlook/v1.0/me/messages

🔐 Authentication
-H "Authorization: Bearer $MATON_API_KEY"

Set API Key
export MATON_API_KEY="YOUR_API_KEY"

🔑 Getting Your API Key
Sign in at https://maton.ai
Go to /settings
Copy your API key
🔗 Connection Management
https://ctrl.maton.ai

📄 List Connections
curl "https://ctrl.maton.ai/connections?app=outlook&status=ACTIVE" \
  -H "Authorization: Bearer $MATON_API_KEY" | jq

➕ Create Connection
curl -X POST https://ctrl.maton.ai/connections \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"app": "outlook"}' | jq

🔍 Get Connection
curl https://ctrl.maton.ai/connections/{connection_id} \
  -H "Authorization: Bearer $MATON_API_KEY" | jq

❌ Delete Connection
curl -X DELETE https://ctrl.maton.ai/connections/{connection_id} \
  -H "Authorization: Bearer $MATON_API_KEY" | jq

🌐 Complete OAuth

Open the returned url in your browser.

🎯 Specify Connection
curl https://gateway.maton.ai/outlook/v1.0/me \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Maton-Connection: CONNECTION_ID" | jq

📚 API Reference
👤 User Profile
curl https://gateway.maton.ai/outlook/v1.0/me \
  -H "Authorization: Bearer $MATON_API_KEY"

📁 Mail Folders
List Mail Folders
curl https://gateway.maton.ai/outlook/v1.0/me/mailFolders \
  -H "Authorization: Bearer $MATON_API_KEY"

Get Mail Folder
curl https://gateway.maton.ai/outlook/v1.0/me/mailFolders/{folderId} \
  -H "Authorization: Bearer $MATON_API_KEY"

Create Mail Folder
curl -X POST https://gateway.maton.ai/outlook/v1.0/me/mailFolders \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"displayName": "My Folder"}'

Delete Mail Folder
curl -X DELETE https://gateway.maton.ai/outlook/v1.0/me/mailFolders/{folderId} \
  -H "Authorization: Bearer $MATON_API_KEY"

List Child Folders
curl https://gateway.maton.ai/outlook/v1.0/me/mailFolders/{folderId}/childFolders \
  -H "Authorization: Bearer $MATON_API_KEY"

📧 Messages
List Messages
curl https://gateway.maton.ai/outlook/v1.0/me/messages \
  -H "Authorization: Bearer $MATON_API_KEY"

From Specific Folder (Inbox)
curl https://gateway.maton.ai/outlook/v1.0/me/mailFolders/Inbox/messages \
  -H "Authorization: Bearer $MATON_API_KEY"

Filter Unread Messages
curl -g "https://gateway.maton.ai/outlook/v1.0/me/messages?\$filter=isRead eq false&\$top=10" \
  -H "Authorization: Bearer $MATON_API_KEY"

Get Message
curl https://gateway.maton.ai/outlook/v1.0/me/messages/{messageId} \
  -H "Authorization: Bearer $MATON_API_KEY"

Create Draft
curl -X POST https://gateway.maton.ai/outlook/v1.0/me/messages \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Hello",
    "body": {
      "contentType": "Text",
      "content": "This is the email body."
    },
    "toRecipients": [
      {
        "emailAddress": {
          "address": "recipient@example.com"
        }
      }
    ]
  }'

Send Message
curl -X POST https://gateway.maton.ai/outlook/v1.0/me/sendMail \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "subject": "Hello",
      "body": {
        "contentType": "Text",
        "content": "This is the email body."
      },
      "toRecipients": [
        {
          "emailAddress": {
            "address": "recipient@example.com"
          }
        }
      ]
    },
    "saveToSentItems": true
  }'

Send Existing Draft
curl -X POST https://gateway.maton.ai/outlook/v1.0/me/messages/{messageId}/send \
  -H "Authorization: Bearer $MATON_API_KEY"

Update Message (Mark as Read)
curl -X PATCH https://gateway.maton.ai/outlook/v1.0/me/messages/{messageId} \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"isRead": true}'

Delete Message
curl -X DELETE https://gateway.maton.ai/outlook/v1.0/me/messages/{messageId} \
  -H "Authorization: Bearer $MATON_API_KEY"

Move Message
curl -X POST https://gateway.maton.ai/outlook/v1.0/me/messages/{messageId}/move \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"destinationId": "FOLDER_ID"}'

📅 Calendar
List Calendars
curl https://gateway.maton.ai/outlook/v1.0/me/calendars \
  -H "Authorization: Bearer $MATON_API_KEY"

List Events
curl https://gateway.maton.ai/outlook/v1.0/me/calendar/events \
  -H "Authorization: Bearer $MATON_API_KEY"

Filter Events by Date
curl -g "https://gateway.maton.ai/outlook/v1.0/me/calendar/events?\$filter=start/dateTime ge '2024-01-01'&\$top=10" \
  -H "Authorization: Bearer $MATON_API_KEY"

Get Event
curl https://gateway.maton.ai/outlook/v1.0/me/events/{eventId} \
  -H "Authorization: Bearer $MATON_API_KEY"

Create Event
curl -X POST https://gateway.maton.ai/outlook/v1.0/me/calendar/events \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Meeting",
    "start": {
      "dateTime": "2024-01-15T10:00:00",
      "timeZone": "UTC"
    },
    "end": {
      "dateTime": "2024-01-15T11:00:00",
      "timeZone": "UTC"
    },
    "attendees": [
      {
        "emailAddress": {
          "address": "attendee@example.com"
        },
        "type": "required"
      }
    ]
  }'

Delete Event
curl -X DELETE https://gateway.maton.ai/outlook/v1.0/me/events/{eventId} \
  -H "Authorization: Bearer $MATON_API_KEY"

👤 Contacts
List Contacts
curl https://gateway.maton.ai/outlook/v1.0/me/contacts \
  -H "Authorization: Bearer $MATON_API_KEY"

Get Contact
curl https://gateway.maton.ai/outlook/v1.0/me/contacts/{contactId} \
  -H "Authorization: Bearer $MATON_API_KEY"

Create Contact
curl -X POST https://gateway.maton.ai/outlook/v1.0/me/contacts \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "givenName": "John",
    "surname": "Doe",
    "emailAddresses": [
      {
        "address": "john.doe@example.com"
      }
    ]
  }'

Delete Contact
curl -X DELETE https://gateway.maton.ai/outlook/v1.0/me/contacts/{contactId} \
  -H "Authorization: Bearer $MATON_API_KEY"

🔍 Query Parameters (OData)

Examples:

$top=10
$filter=isRead eq false
$orderby=receivedDateTime desc
$search="keyword"

⚠️ Notes
Use me for authenticated user
Content types: Text or HTML
Folder names: Inbox, Drafts, SentItems, etc.
Use ISO 8601 for datetime
Important
# Use -g when URL contains $ or []
curl -g "URL"

❌ Errors
Code	Meaning
400	Missing Outlook connection
401	Invalid API key
429	Rate limited (10 req/sec)
🛠 Troubleshooting
Check API Key
echo $MATON_API_KEY

Test Auth
curl https://ctrl.maton.ai/connections \
  -H "Authorization: Bearer $MATON_API_KEY" | jq