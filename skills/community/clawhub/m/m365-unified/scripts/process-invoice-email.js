#!/usr/bin/env node
/**
 * Process Invoice Email
 * 
 * Workflow:
 * 1. Find email with invoice (subject: "Rechnung")
 * 2. Extract vendor & invoice number from subject + body
 * 3. Save attachment to SharePoint: /Buchhaltung/Rechnungen/{Vendor}_{InvoiceNumber}.pdf
 * 4. Mark email as read
 * 5. Move email to folder: Inbox/Invoices/
 */

import dotenv from 'dotenv';
import { createM365Client } from '../src/index.js';
import { Client } from '@microsoft/microsoft-graph-client';
import { getAccessToken } from '../src/auth/graph-client.js';
import axios from 'axios';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const rootDir = resolve(__dirname, '../../..');
dotenv.config({ path: resolve(rootDir, '.env'), override: true });

async function processInvoiceEmail() {
  console.log('📧 Processing Invoice Email\n');
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

    // Find first email with attachments (prefer unread)
    let targetEmail = null;
    for (const email of emails) {
      if (email.hasAttachments) {
        const atts = await client.email.listAttachments(email.id);
        if (atts.length > 0) {
          targetEmail = email;
          if (!email.isRead) break; // Prefer unread
        }
      }
    }
    
    if (!targetEmail) {
      console.log('ℹ️  No emails with attachments found\n');
      return;
    }
    
    console.log('📄 Processing email:');
    console.log(`   Subject: ${targetEmail.subject}`);
    console.log(`   From: ${targetEmail.from?.emailAddress?.address}`);
    console.log(`   IsRead: ${targetEmail.isRead}`);
    console.log('');

    // Get full email body for better extraction
    const fullEmail = await client.email.get(targetEmail.id, { includeBody: true });
    const bodyText = fullEmail.body?.content || '';
    const bodyPreview = fullEmail.bodyPreview || '';
    console.log('📧 Body preview:', bodyPreview.substring(0, 150));
    console.log('');

    // Step 2: Extract vendor and invoice number from subject + body
    console.log('2️⃣ Extracting invoice data...');
    
    const subject = targetEmail.subject;
    const searchText = `${subject} ${bodyText} ${bodyPreview}`;
    
    // Extract invoice number
    let invoiceNumber = 'UNBEKANNT';
    const invoicePatterns = [
      /Rechnungsnummer[:\s]*([A-Z0-9-]+)/i,
      /Rechnung[\s#:]*([A-Z0-9-]+)/i,
      /Invoice[\s#:]*([0-9A-Z-]+)/i,
      /Beleg[\s#:]*([0-9-]+)/i,
      /Nr\.[\s:]*([A-Z0-9-]+)/i,
    ];
    
    for (const pattern of invoicePatterns) {
      const match = searchText.match(pattern);
      if (match) {
        invoiceNumber = match[1].trim();
        console.log(`   Invoice Number (raw): ${invoiceNumber}`);
        break;
      }
    }
    
    // PROBLEM #2 FIX: Validierung - Rechnungsnummer muss mindestens eine Ziffer enthalten
    if (invoiceNumber !== 'UNBEKANNT') {
      const hasDigit = /\d/.test(invoiceNumber);
      if (!hasDigit) {
        console.log(`   ⚠️  Invoice number "${invoiceNumber}" has no digits - using fallback`);
        invoiceNumber = 'UNBEKANNT';
      } else {
        console.log(`   ✅ Invoice number contains digit(s): ${invoiceNumber}`);
      }
    }
    
    // Extract vendor
    let vendor = 'Unbekannt';
    
    // Try body first - look for company names or "von" patterns
    const vendorPatterns = [
      /(?:von|from|Absender|Herausgeber)[:\s]*([A-Za-zäöüÄÖÜß][a-zA-ZäöüÄÖÜß\s]+?)(?:\n|$)/i,
      /(?:Firma|Company|Lieferant)[:\s]*([A-Za-zäöüÄÖÜß][a-zA-ZäöüÄÖÜß\s]+?)(?:\n|$)/i,
      /^([A-Z][a-zA-ZäöüÄÖÜß\s]+)(?:\s*GmbH|\s*AG|\s*Co\.|\s*KG)/,
    ];
    
    for (const pattern of vendorPatterns) {
      const match = searchText.match(pattern);
      if (match && match[1]) {
        vendor = match[1].trim().substring(0, 30);
        console.log(`   Vendor: ${vendor} (from body)`);
        break;
      }
    }
    
    // Fallback: Extract from sender email - use DOMAIN name, not local part
    if (vendor === 'Unbekannt' && targetEmail.from?.emailAddress?.address) {
      const emailParts = targetEmail.from.emailAddress.address.split('@');
      if (emailParts.length > 1) {
        // Use domain (after @), remove TLD for cleaner name
        const domain = emailParts[1]; // e.g., "example.com"
        const domainWithoutTld = domain.split('.')[0]; // e.g., "example"
        vendor = domainWithoutTld.toUpperCase(); // e.g., "EXAMPLE"
        console.log(`   Vendor: ${vendor} (from domain)`);
      }
    }
    
    // Sanitize for filename
    vendor = vendor.replace(/[^a-zA-Z0-9äöüÄÖÜß_-]/g, '_').replace(/_+/g, '_');
    invoiceNumber = invoiceNumber.replace(/[^A-Z0-9-]/gi, '');
    
    console.log(`   Final before attachment fallback: ${vendor}_${invoiceNumber}\n`);

    // Step 3: Get attachments
    console.log('3️⃣ Getting attachments...');
    const attachments = await client.email.listAttachments(targetEmail.id);
    console.log(`   Found ${attachments.length} attachment(s)\n`);

    const savedFiles = [];
    let extractedInvoiceNumber = invoiceNumber; // Store original extracted value
    let extractedVendor = vendor; // Store original extracted value
    
    for (const attachment of attachments) {
      console.log(`   📎 ${attachment.name} (${(attachment.size / 1024).toFixed(1)} KB)`);
      
      // Download attachment using axios
      const token = await client._token;
      const downloadUrl = `https://graph.microsoft.com/v1.0/users/${process.env.M365_MAILBOX}/messages/${targetEmail.id}/attachments/${attachment.id}/$value`;
      const response = await axios.get(downloadUrl, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        responseType: 'arraybuffer',
      });
      
      const content = Buffer.from(response.data);
      console.log(`      Downloaded ${content.length} bytes`);
      
      // Create new filename
      const ext = attachment.name.split('.').pop() || 'pdf';
      const nameWithoutExt = attachment.name.substring(0, attachment.name.lastIndexOf('.')) || attachment.name;
      
      // Use extracted invoice number OR fallback to filename (without extension)
      let finalInvoiceNumber = extractedInvoiceNumber;
      
      // Fallback wenn keine Rechnungsnummer gefunden wurde
      if (!finalInvoiceNumber || finalInvoiceNumber === 'UNBEKANNT' || finalInvoiceNumber.trim() === '') {
        // Fallback: Verwende Dateiname als Rechnungsnummer
        finalInvoiceNumber = nameWithoutExt.replace(/[^A-Z0-9_-]/gi, '_').toUpperCase();
        console.log(`      → Using filename as invoice number: ${finalInvoiceNumber}`);
      } else {
        console.log(`      → Using extracted invoice number: ${finalInvoiceNumber}`);
      }
      
      const newFilename = `${extractedVendor}_${finalInvoiceNumber}.${ext}`;
      
      // Save to SharePoint
      const sharepointPath = `/Buchhaltung/Rechnungen/${newFilename}`;
      const uploaded = await client.sharepoint.upload(sharepointPath, content, {
        contentType: attachment.contentType || 'application/octet-stream',
      });
      
      console.log(`      ✅ Saved to SharePoint: ${sharepointPath}`);
      savedFiles.push(sharepointPath);
      
      // PROBLEM #1 FIX: Update extractedInvoiceNumber with final value for output
      extractedInvoiceNumber = finalInvoiceNumber;
    }
    console.log('');

    // Step 4: Mark email as read
    console.log('4️⃣ Marking email as read...');
    await client.email.markAsRead(targetEmail.id);
    console.log('   ✅ Email marked as read\n');

    // Step 5: Find or create destination folder in Inbox
    console.log('5️⃣ Finding destination folder in Inbox...');
    const folders = await client.folders.list();
    
    const inbox = folders.find(f => f.displayName === 'Inbox' || f.displayName === 'Posteingang');
    if (!inbox) {
      console.log('   ❌ Inbox not found!');
      return;
    }
    console.log(`   ✅ Found Inbox: ${inbox.displayName}`);
    
    // Get child folders
    const token = await client._token;
    const childFoldersResponse = await axios.get(
      `https://graph.microsoft.com/v1.0/users/${process.env.M365_MAILBOX}/mailFolders/${inbox.id}/childFolders`,
      { headers: { 'Authorization': `Bearer ${token}` } }
    );
    const childFolders = childFoldersResponse.data.value || [];
    
    console.log(`   Child folders: ${childFolders.length}`);
    
    let invoicesFolder = childFolders.find(f => f.displayName === 'Invoices' || f.displayName === 'Rechnungen');
    if (!invoicesFolder) {
      console.log('   ❌ Invoices folder not found!');
      return;
    }
    console.log(`   ✅ Found: ${invoicesFolder.displayName}\n`);
    
    // Step 6: Move email to folder
    console.log('6️⃣ Moving email to folder...');
    const movedEmail = await client.email.move(targetEmail.id, invoicesFolder.id);
    console.log(`   ✅ Email moved to Inbox/Invoices\n`);

    console.log('✅ Invoice processing complete!\n');
    console.log('='.repeat(60));
    console.log('\n📋 Summary:');
    console.log(`   Email: ${targetEmail.subject}`);
    console.log(`   Attachments saved: ${savedFiles.length}`);
    console.log(`   Filename pattern: ${vendor}_${invoiceNumber}`);
    console.log(`   Email marked as read: ✅`);
    console.log(`   Email moved: ✅\n`);
    
    // PROBLEM #1 FIX: Output the FINAL values (after attachment fallback)
    console.log('\n' + '='.repeat(60));
    console.log('OUTPUT_FOR_WEBHOOK_HANDLER:');
    console.log(`Lieferant: ${extractedVendor}`);
    console.log(`Rechnungsnummer: ${extractedInvoiceNumber}`);
    console.log('='.repeat(60) + '\n');

  } catch (error) {
    console.error('❌ Error:', error.message);
    if (error.stack) {
      console.error('   Stack:', error.stack.split('\n').slice(0, 3).join('\n   '));
    }
    process.exit(1);
  }
}

processInvoiceEmail();
