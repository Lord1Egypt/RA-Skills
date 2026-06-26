# DocuScan Dashboard Companion Kit

## Your Personal Document Vault
Access all your scanned documents in one beautiful, searchable dashboard. Find that receipt from last March or the contract from Tuesday just by typing a keyword.

## Internal Build Spec

### UI/UX
- Clean, grid-based interface built with Next.js and shadcn/ui.
- Thumbnail previews for all PDFs.

### Features
1. **Document Library:** Grid and list views to easily browse all scanned documents.
2. **Universal Search:** Full-text search across the content of all scanned documents (powered by the LLM's initial extraction payload stored in the local DB).
3. **Tagging & Folders:** Auto-tags generated during the scan (e.g., `#receipt`, `#contract`, `#handwritten`) with manual overrides available.
4. **Scan History:** Timeline view of processed documents to easily find your most recent scans.

### Database Schema (Local SQLite/Supabase)
```sql
CREATE TABLE scans (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL,
  filename VARCHAR(255) NOT NULL,
  document_type VARCHAR(100), -- receipt, contract, handwriting, etc.
  extracted_markdown TEXT NOT NULL,
  pdf_path VARCHAR(255) NOT NULL,
  thumbnail_path VARCHAR(255),
  tags JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Design System Tokens
- **Colors:**
  - Primary: `hsl(222.2 47.4% 11.2%)`
  - Accent: `hsl(210 40% 96.1%)`
  - Foreground: `hsl(222.2 84% 4.9%)`
  - Muted: `hsl(210 40% 96.1%)`
- **Typography:**
  - Sans-serif for UI (Inter, default shadcn/ui)
  - Serif for Formal Document Previews (Merriweather)
- **Border Radius:** `0.5rem` (rounded-md)

## ⚠️ Security Requirements
- **Authentication:** Implement user authentication before deploying. No anonymous access to scanned documents.
- **Row Level Security (RLS):** Enable Supabase RLS on all tables. Users must only see their own documents.
- **Encryption at Rest:** The `extracted_markdown` field will contain sensitive document text (financial records, contracts, medical documents). Enable column-level encryption or ensure Supabase's at-rest encryption covers this data.
- **File Storage:** Store scanned PDFs in a **private** storage bucket with signed URLs. Never expose document files publicly.
- **Environment Variables:** All Supabase keys, API URLs, and auth secrets must be stored as environment variables — never hardcoded.
- **Sensitive Documents:** If users scan financial, medical, or legal documents, remind them that the dashboard stores extracted text. They should evaluate their own compliance requirements (HIPAA, PCI, etc.).
