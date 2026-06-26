# Paperless-ngx API Endpoints

This file is a placeholder for detailed information about Paperless-ngx API endpoints.

Once the official API documentation is accessible, this file should be updated with:

- Authentication details (if different from token header)
- Document upload endpoint and expected data format (e.g., `/api/documents/`)
- Document categorization/tagging endpoints (e.g., for updating existing documents)
- Endpoints for listing existing tags/document types (useful for categorization)
- Examples of request/response bodies.

**Commonly expected endpoints:**

- `POST /api/documents/`: Upload a new document.
- `GET /api/documents/{id}/`: Retrieve document details.
- `PATCH /api/documents/{id}/`: Update document properties (including tags, document type).
- `GET /api/tags/`: List all available tags.
- `POST /api/tags/`: Create a new tag.
- `GET /api/document_types/`: List all available document types.
- `POST /api/document_types/`: Create a new document type.
