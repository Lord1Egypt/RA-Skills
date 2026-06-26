/**
 * Exchange Online - Mail Operations
 * 
 * Send, receive, move, delete emails and manage attachments.
 */

/**
 * Send an email
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @param {Object} message - Message object
 * @param {string} message.subject - Email subject
 * @param {string} message.body - Email body (HTML or text)
 * @param {string} [message.bodyType='HTML'] - Body content type
 * @param {Array} message.toRecipients || message.to || [] - Array of recipient email addresses
 * @param {Array} [message.ccRecipients] - CC recipients
 * @param {Array} [message.bccRecipients] - BCC recipients
 * @param {Array} [message.attachments] - Attachments (name, contentType, contentBytes)
 * @param {Array} [message.importance='normal'] - Importance (low, normal, high)
 * @returns {Promise<void>}
 */
export async function sendMail(graphClient, mailbox, message) {
  const requestBody = {
    message: {
      subject: message.subject,
      body: {
        contentType: message.bodyType || 'HTML',
        content: message.body,
      },
      importance: message.importance || 'normal',
      toRecipients: (message.toRecipients || message.to || []).map(email => ({
        emailAddress: { address: email },
      })),
    },
  };

  // Add CC recipients if provided
  if (message.ccRecipients?.length) {
    requestBody.message.ccRecipients = message.ccRecipients.map(email => ({
      emailAddress: { address: email },
    }));
  }

  // Add BCC recipients if provided
  if (message.bccRecipients?.length) {
    requestBody.message.bccRecipients = message.bccRecipients.map(email => ({
      emailAddress: { address: email },
    }));
  }

  // Add attachments if provided
  if (message.attachments?.length) {
    requestBody.message.attachments = message.attachments.map(att => ({
      '@odata.type': '#microsoft.graph.fileAttachment',
      name: att.name,
      contentType: att.contentType,
      contentBytes: att.contentBytes,
    }));
  }

  return graphClient.api(`/users/${mailbox}/sendMail`).post(requestBody);
}

/**
 * List messages in mailbox
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @param {Object} [options] - Query options
 * @param {number} [options.top=10] - Number of messages to retrieve
 * @param {string} [options.folder='inbox'] - Folder to query (inbox, sentitems, drafts, deleteditems)
 * @param {string} [options.select] - Fields to select
 * @param {string} [options.orderBy] - Order by field (e.g., 'receivedDateTime desc')
 * @param {string} [options.filter] - OData filter
 * @returns {Promise<Array>} List of messages
 */
export async function listMessages(graphClient, mailbox, options = {}) {
  const { top = 10, folder = 'inbox', select, orderBy, filter } = options;

  let endpoint = `/users/${mailbox}/mailFolders/${folder}/messages`;
  
  const queryParams = new URLSearchParams();
  queryParams.append('$top', top);
  
  if (select) queryParams.append('$select', select);
  if (orderBy) queryParams.append('$orderby', orderBy);
  if (filter) queryParams.append('$filter', filter);

  const queryString = queryParams.toString();
  if (queryString) endpoint += `?${queryString}`;

  const response = await graphClient.api(endpoint).get();
  return response.value;
}

/**
 * Get a specific message
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @param {string} messageId - Message ID
 * @param {Object} [options] - Query options
 * @param {boolean} [options.includeBody=true] - Include message body
 * @param {string} [options.select] - Fields to select
 * @returns {Promise<Object>} Message object
 */
export async function getMessage(graphClient, mailbox, messageId, options = {}) {
  const { includeBody = true } = options;
  
  let select = options.select || 'id,subject,from,toRecipients,ccRecipients,receivedDateTime,bodyPreview,hasAttachments';
  if (includeBody && !select.includes('body')) {
    select += ',body';
  }

  return graphClient.api(`/users/${mailbox}/messages/${messageId}`)
    .query({ $select: select })
    .get();
}

/**
 * Move a message to another folder
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @param {string} messageId - Message ID
 * @param {string} destinationFolderId - Destination folder ID
 * @returns {Promise<Object>} Moved message
 */
export async function moveMessage(graphClient, mailbox, messageId, destinationFolderId) {
  return graphClient.api(`/users/${mailbox}/messages/${messageId}/move`)
    .post({ destinationId: destinationFolderId });
}

/**
 * Delete a message
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @param {string} messageId - Message ID
 * @returns {Promise<void>}
 */
export async function deleteMessage(graphClient, mailbox, messageId) {
  return graphClient.api(`/users/${mailbox}/messages/${messageId}`).delete();
}

/**
 * Search messages using Microsoft Graph search
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @param {string} query - Search query (KQL syntax)
 * @param {Object} [options] - Query options
 * @param {number} [options.top=10] - Max results
 * @param {string} [options.select] - Fields to select
 * @returns {Promise<Array>} Matching messages
 */
export async function searchMessages(graphClient, mailbox, query, options = {}) {
  const { top = 10, select } = options;
  
  const queryParams = new URLSearchParams();
  queryParams.append('$search', `"${query}"`);
  queryParams.append('$top', top);
  if (select) queryParams.append('$select', select);

  const response = await graphClient.api(`/users/${mailbox}/messages`)
    .query(queryParams)
    .get();
  
  return response.value;
}

/**
 * List attachments for a message
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @param {string} messageId - Message ID
 * @returns {Promise<Array>} List of attachments
 */
export async function listAttachments(graphClient, mailbox, messageId) {
  const response = await graphClient.api(`/users/${mailbox}/messages/${messageId}/attachments`).get();
  return response.value;
}

/**
 * Get attachment metadata
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @param {string} messageId - Message ID
 * @param {string} attachmentId - Attachment ID
 * @returns {Promise<Object>} Attachment metadata
 */
export async function getAttachment(graphClient, mailbox, messageId, attachmentId) {
  return graphClient.api(`/users/${mailbox}/messages/${messageId}/attachments/${attachmentId}`).get();
}

/**
 * Download attachment content (binary)
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @param {string} messageId - Message ID
 * @param {string} attachmentId - Attachment ID
 * @returns {Promise<Buffer>} Attachment binary content
 */
export async function downloadAttachment(graphClient, mailbox, messageId, attachmentId) {
  const response = await graphClient.api(`/users/${mailbox}/messages/${messageId}/attachments/${attachmentId}/$value`).get();
  return response; // Binary content
}

/**
 * Save email attachment to SharePoint
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @param {string} sharepointSiteId - SharePoint site ID
 * @param {string} messageId - Message ID
 * @param {string} attachmentId - Attachment ID
 * @param {string} sharepointPath - Destination path in SharePoint (e.g., '/Documents/Invoices')
 * @returns {Promise<Object>} Upload result
 */
export async function saveAttachmentToSharePoint(graphClient, mailbox, sharepointSiteId, messageId, attachmentId, sharepointPath) {
  // Step 1: Get attachment metadata
  const attachment = await getAttachment(graphClient, mailbox, messageId, attachmentId);

  // Step 2: Download attachment content
  const content = await downloadAttachment(graphClient, mailbox, messageId, attachmentId);

  // Step 3: Upload to SharePoint
  const uploadPath = `${sharepointPath}/${attachment.name}`;
  
  // Import SharePoint module dynamically to avoid circular dependency
  const { uploadFile } = await import('../sharepoint/files.js');
  const result = await uploadFile(graphClient, sharepointSiteId, uploadPath, content, {
    contentType: attachment.contentType,
    conflict: 'replace',
  });

  return {
    success: true,
    fileName: attachment.name,
    fileSize: attachment.size,
    sharepointPath: uploadPath,
    sharepointUrl: result.webUrl,
    uploadedAt: new Date().toISOString(),
  };
}

/**
 * Mark a message as read
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @param {string} messageId - Message ID
 * @returns {Promise<void>}
 */
export async function markAsRead(graphClient, mailbox, messageId) {
  return graphClient.api(`/users/${mailbox}/messages/${messageId}`)
    .patch({ isRead: true });
}

/**
 * Mark a message as unread
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @param {string} messageId - Message ID
 * @returns {Promise<void>}
 */
export async function markAsUnread(graphClient, mailbox, messageId) {
  return graphClient.api(`/users/${mailbox}/messages/${messageId}`)
    .patch({ isRead: false });
}

/**
 * Reply to a message
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @param {string} messageId - Message ID
 * @param {string} body - Reply body
 * @param {string} [bodyType='HTML'] - Body content type
 * @returns {Promise<void>}
 */
export async function replyToMessage(graphClient, mailbox, messageId, body, bodyType = 'HTML') {
  return graphClient.api(`/users/${mailbox}/messages/${messageId}/reply`)
    .post({
      message: {
        body: {
          contentType: bodyType,
          content: body,
        },
      },
    });
}

/**
 * Forward a message
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @param {string} messageId - Message ID
 * @param {Array} toRecipients - Recipients to forward to
 * @param {string} [comment] - Optional comment
 * @returns {Promise<void>}
 */
export async function forwardMessage(graphClient, mailbox, messageId, toRecipients, comment = '') {
  return graphClient.api(`/users/${mailbox}/messages/${messageId}/forward`)
    .post({
      comment,
      toRecipients: toRecipients.map(email => ({
        emailAddress: { address: email },
      })),
    });
}
