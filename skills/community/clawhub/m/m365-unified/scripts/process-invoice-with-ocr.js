#!/usr/bin/env node
/**
 * Process Invoice Email with PDF Text Extraction
 * 
 * Workflow:
 * 1. Find email with invoice (subject: "Rechnung")
 * 2. Download PDF attachment
 * 3. Extract text from PDF (vendor + invoice number)
 * 4. Save to SharePoint with new name: {Vendor}_{InvoiceNumber}.pdf
 * 5. Mark email as read
 * 6. Move email to folder: Posteingang/1_MerkelDesign/0.1_Rechnungen/
 */

import dotenv from 'dotenv';
import { createM365Client } from '../src/index.js';
import { Client } from '@microsoft/microsoft-graph-client';
import { getAccessToken } from '../src/auth/graph-client.js';
import axios from 'axios';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';
import { execSync } from 'child_process';
import fs from 'fs';
import { writeFileSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const rootDir = resolve(__dirname, '../../..');
dotenv.config({ path: resolve(rootDir, '.env'), override: true });

/**
 * Extract text from PDF using pypdf
 */
function extractTextFromPDF(pdfBuffer) {
  try {
    // Write temp file
    const tempPath = `/tmp/invoice_temp_${Date.now()}.pdf`;
    writeFileSync(tempPath, pdfBuffer);
    
    // Extract text using Python with explicit path
    const pythonScript = `
import sys
sys.path.insert(0, '/home/linuxbrew/.linuxbrew/lib/python3.14/site-packages')
from pypdf import PdfReader

try:
    reader = PdfReader('${tempPath}')
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    print(text)
except Exception as e:
    print(f'ERROR: {e}', file=sys.stderr)
    sys.exit(1)
`;
    
    const result = execSync(`python3 -c "${pythonScript}"`, {
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'pipe']
    });
    
    // Cleanup
    fs.unlinkSync(tempPath);
    
    return result.trim();
  } catch (error) {
    console.error('❌ PDF extraction failed:', error.message);
    if (error.stderr) {
      console.error('   stderr:', error.stderr.toString().substring(0, 500));
    }
    return null;
  }
}

/**
 * Extract vendor and invoice number from PDF text
 */
function extractInvoiceData(text) {
  if (!text) return { vendor: 'Unbekannt', invoiceNumber: 'UNBEKANNT' };
  
  console.log('   📄 PDF Text extracted (~' + text.length + ' chars)');
  console.log('   First 200 chars:', text.substring(0, 200).replace(/\n/g, ' '));
  console.log('');
  
  // Try to find invoice number
  let invoiceNumber = 'UNBEKANNT';
  const invoicePatterns = [
    /Rechnungsnummer[:\s]*([A-Z0-9-]+)/i,
    /Invoice[\s#:]*([0-9A-Z-]+)/i,
    /Beleg[\s#:]*([0-9-]+)/i,
    /Nr\.[\s:]*([A-Z0-9-]+)/i,
    /Nummer[\s#:]*([A-Z0-9-]+)/i,
    /Rechnung[\s#:]*([A-Z0-9-]+)/i,
  ];
  
  for (const pattern of invoicePatterns) {
    const match = text.match(pattern);
    if (match) {
      invoiceNumber = match[1].trim();
      console.log(`   ✅ Invoice Number found: ${invoiceNumber}`);
      break;
    }
  }
  
  // Try to find vendor (company name) - look for "Rechnungsempfänger" or similar
  let vendor = 'Unbekannt';
  
  // Pattern 1: Rechnungsempfänger (invoice recipient)
  const recipientMatch = text.match(/Rechnungsempfänger[:\s]*([A-Za-zäöüÄÖÜß\s]+?)(?:\n|$)/i);
  if (recipientMatch && recipientMatch[1]) {
    vendor = recipientMatch[1].trim().split('\n')[0].substring(0, 30);
    console.log(`   ✅ Vendor from recipient: ${vendor}`);
  }
  
  // Pattern 2: Company at start of document (before "Rechnung")
  if (vendor === 'Unbekannt') {
    const headerMatch = text.match(/^([A-Z][a-zA-ZäöüÄÖÜß\s]+)(?:\s*GmbH|\s*AG|\s*Co\.|\s*KG)?[\s\n]/);
    if (headerMatch && headerMatch[1]) {
      vendor = headerMatch[1].trim();
      console.log(`   ✅ Vendor from header: ${vendor}`);
    }
  }
  
  // Pattern 3: "Von" or "Absender"
  if (vendor === 'Unbekannt') {
    const fromMatch = text.match(/(?:Von|Absender|Herausgeber)[:\s]*([A-Za-zäöüÄÖÜß\s]+?)(?:\n|$)/i);
    if (fromMatch && fromMatch[1]) {
      vendor = fromMatch[1].trim();
      console.log(`   ✅ Vendor from sender: ${vendor}`);
    }
  }
  
  // Fallback: Use first meaningful capitalized word
  if (vendor === 'Unbekannt') {
    const words = text.split(/[\s\n]+/);
    for (const word of words) {
      if (/^[A-Z][a-z]{2,}$/.test(word) && 
          !['Der', 'Die', 'Das', 'Und', 'Mit', 'Von', 'Zum', 'Zur', 'Rechnung', 'Herr', 'Frau', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'].includes(word)) {
        vendor = word;
        console.log(`   ℹ️  Vendor fallback: ${vendor}`);
        break;
      }
    }
  }
  
  // Sanitize for filename
  vendor = vendor.replace(/[^a-zA-Z0-9äöüÄÖÜß_-]/g, '_').replace(/_+/g, '_');
  invoiceNumber = invoiceNumber.replace(/[^A-Z0-9-]/gi, '');
  
  console.log(`   Final - Vendor: ${vendor}, Invoice: ${invoiceNumber}`);
  
  return { vendor, invoiceNumber };
}

async function processInvoiceWithOCR() {
  console.log('📧 Processing Invoice with PDF Text Extraction\n');
  console.log('='.repeat(60));

  const client = await createM365Client({
    tenantId: process.env.M365_TENANT_ID,
    clientId: process.env.M365_CLIENT_ID,
    clientSecret: process.env.M365_CLIENT_SECRET,
    mailbox: process.env.M365_MAILBOX,
    sharepointSiteId: process.env.M365_SHAREPOINT_SITE_ID?.replace(/"/g, ''),
    enableEmail: true,
    enableSharepoint: process.env.M365_ENABLE_SHAREPOINT === 'true',
  });

  try {
    // Step 1: Search for invoice emails
    console.log('\n1️⃣ Searching for invoice emails...');
    const searchQuery = 'subject:Rechnung';
    const emails = await client.email.search(searchQuery, {
      top: 20,
      select: 'id,subject,from,receivedDateTime,isRead,hasAttachments',
    });

    console.log(`   Found ${emails.length} email(s) with "Rechnung" in subject\n`);

    // Find first email with actual attachments
    let targetEmail = null;
    for (const email of emails) {
      if (email.hasAttachments) {
        const attachments = await client.email.listAttachments(email.id);
        if (attachments.length > 0 && attachments[0].contentType?.includes('pdf')) {
          targetEmail = email;
          console.log(`   ✅ Found email with PDF attachment: ${email.subject}\n`);
          break;
        }
      }
    }

    if (!targetEmail) {
      console.log('ℹ️  No invoice emails with PDF attachments found\n');
      return;
    }
    
    console.log('📄 Processing email:');
    console.log(`   Subject: ${targetEmail.subject}`);
    console.log(`   From: ${targetEmail.from?.emailAddress?.address}`);
    console.log(`   HasAttachments: ${targetEmail.hasAttachments}`);
    console.log('');

    if (!targetEmail.hasAttachments) {
      console.log('⚠️  Email reports no attachments - skipping\n');
      return;
    }

    // Double-check attachments
    const attachments = await client.email.listAttachments(targetEmail.id);
    console.log(`   Actual attachments: ${attachments.length}\n`);
    
    if (attachments.length === 0) {
      console.log('   ⚠️  No actual attachments found - skipping\n');
      return;
    }
    const attachment = attachments[0];
    console.log(`   📎 ${attachment.name} (${(attachment.size / 1024).toFixed(1)} KB)\n`);

    // Step 3: Download PDF
    console.log('3️⃣ Downloading PDF...');
    const token = await client._token;
    const downloadUrl = `https://graph.microsoft.com/v1.0/users/${process.env.M365_MAILBOX}/messages/${targetEmail.id}/attachments/${attachment.id}/$value`;
    const response = await axios.get(downloadUrl, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      responseType: 'arraybuffer',
    });
    
    const pdfBuffer = Buffer.from(response.data);
    console.log(`   ✅ Downloaded ${pdfBuffer.length} bytes\n`);

    // Step 4: Extract text from PDF
    console.log('4️⃣ Extracting text from PDF...');
    const pdfText = extractTextFromPDF(pdfBuffer);
    
    // Step 5: Parse vendor and invoice number
    console.log('5️⃣ Parsing invoice data...');
    const { vendor, invoiceNumber } = extractInvoiceData(pdfText);
    console.log(`   Vendor: ${vendor}`);
    console.log(`   Invoice Number: ${invoiceNumber}\n`);

    // Step 6: Create new filename
    const ext = attachment.name.split('.').pop() || 'pdf';
    const newFilename = `${vendor}_${invoiceNumber}.${ext}`;
    console.log(`   📝 New filename: ${newFilename}\n`);

    // Step 7: Save to SharePoint
    console.log('6️⃣ Saving to SharePoint...');
    const sharepointPath = `/2_Buchhaltung/Rechnungen (Eingang)/${newFilename}`;
    const uploaded = await client.sharepoint.upload(sharepointPath, pdfBuffer, {
      contentType: 'application/pdf',
    });
    
    console.log(`   ✅ Saved to: ${sharepointPath}\n`);

    // Step 8: Mark email as read
    console.log('7️⃣ Marking email as read...');
    await client.email.markAsRead(targetEmail.id);
    console.log('   ✅ Email marked as read\n');

    // Step 9: Move email to folder
    console.log('8️⃣ Moving email to folder...');
    const folders = await client.folders.list();
    const inbox = folders.find(f => f.displayName === 'Posteingang');
    
    if (!inbox) {
      console.log('   ❌ Posteingang not found!');
      return;
    }

    // Get child folders
    const childFoldersResponse = await axios.get(
      `https://graph.microsoft.com/v1.0/users/${process.env.M365_MAILBOX}/mailFolders/${inbox.id}/childFolders`,
      {
        headers: { 'Authorization': `Bearer ${token}` },
      }
    );
    const childFolders = childFoldersResponse.data.value || [];
    
    let merkelDesignFolder = childFolders.find(f => f.displayName === '1_MerkelDesign');
    if (!merkelDesignFolder) {
      console.log('   ❌ 1_MerkelDesign folder not found!');
      return;
    }

    // Get subfolders
    const mdChildFoldersResponse = await axios.get(
      `https://graph.microsoft.com/v1.0/users/${process.env.M365_MAILBOX}/mailFolders/${merkelDesignFolder.id}/childFolders`,
      {
        headers: { 'Authorization': `Bearer ${token}` },
      }
    );
    const mdChildFolders = mdChildFoldersResponse.data.value || [];
    
    let rechnungenFolder = mdChildFolders.find(f => f.displayName === '0.1_Rechnungen');
    if (!rechnungenFolder) {
      console.log('   ❌ 0.1_Rechnungen folder not found!');
      return;
    }

    await client.email.move(targetEmail.id, rechnungenFolder.id);
    console.log(`   ✅ Email moved to Posteingang/1_MerkelDesign/0.1_Rechnungen\n`);

    console.log('✅ Invoice processing complete!\n');
    console.log('='.repeat(60));
    console.log('\n📋 Summary:');
    console.log(`   Email: ${targetEmail.subject}`);
    console.log(`   Original filename: ${attachment.name}`);
    console.log(`   New filename: ${newFilename}`);
    console.log(`   Vendor: ${vendor}`);
    console.log(`   Invoice Number: ${invoiceNumber}`);
    console.log(`   SharePoint: ${sharepointPath}`);
    console.log(`   Email moved: ✅\n`);

  } catch (error) {
    console.error('❌ Error:', error.message);
    if (error.stack) {
      console.error('   Stack:', error.stack.split('\n').slice(0, 3).join('\n   '));
    }
    process.exit(1);
  }
}

processInvoiceWithOCR();
