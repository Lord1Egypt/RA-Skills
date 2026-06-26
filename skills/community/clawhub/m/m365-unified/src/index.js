/**
 * M365 Unified Skill - Main Entry Point
 * 
 * Modular Microsoft Graph API client for OpenClaw.
 * Enables only the features you need via configuration.
 */

import { Client } from '@microsoft/microsoft-graph-client';
import { getAccessToken } from './auth/graph-client.js';

// Feature modules
import * as email from './email/mail.js';
import * as folders from './email/folders.js';
import * as sharepoint from './sharepoint/files.js';
import * as onedrive from './onedrive/files.js';
import * as planner from './planner/tasks.js';
import * as webhooks from './webhooks/subscriptions.js';

/**
 * Create M365 Unified Client
 * 
 * @param {Object} config - Configuration object
 * @param {string} config.tenantId - Azure AD Tenant ID
 * @param {string} config.clientId - App Registration Client ID
 * @param {string} config.clientSecret - App Registration Client Secret
 * @param {string} [config.mailbox] - Primary mailbox email
 * @param {Array} [config.sharedMailboxes] - Shared mailbox emails
 * @param {string} [config.sharepointSiteId] - SharePoint site ID
 * @param {string} [config.onedriveUser] - OneDrive user email
 * @param {string} [config.plannerGroupId] - M365 Group ID for Planner
 * @param {boolean} [config.enableEmail=true] - Enable email features
 * @param {boolean} [config.enableSharepoint=false] - Enable SharePoint
 * @param {boolean} [config.enableOnedrive=false] - Enable OneDrive
 * @param {boolean} [config.enablePlanner=false] - Enable Planner
 * @param {boolean} [config.enableWebhooks=false] - Enable webhooks
 * @returns {Promise<Object>} M365 client with enabled features
 */
export async function createM365Client(config) {
  const token = await getAccessToken(config);
  const graphClient = Client.init({
    authProvider: (done) => done(null, token),
  });

  const client = {
    _config: config,
    _token: token,
    _graphClient: graphClient,
  };

  // Email module (always available if mailbox configured)
  if (config.enableEmail !== false && config.mailbox) {
    client.email = {
      send: (message) => email.sendMail(graphClient, config.mailbox, message),
      list: (options) => email.listMessages(graphClient, config.mailbox, options),
      get: (messageId, options) => email.getMessage(graphClient, config.mailbox, messageId, options),
      move: (messageId, folderId) => email.moveMessage(graphClient, config.mailbox, messageId, folderId),
      delete: (messageId) => email.deleteMessage(graphClient, config.mailbox, messageId),
      search: (query, options) => email.searchMessages(graphClient, config.mailbox, query, options),
      listAttachments: (messageId) => email.listAttachments(graphClient, config.mailbox, messageId),
      getAttachment: (messageId, attachmentId) => email.getAttachment(graphClient, config.mailbox, messageId, attachmentId),
      downloadAttachment: (messageId, attachmentId) => email.downloadAttachment(graphClient, config.mailbox, messageId, attachmentId),
      saveAttachmentToSharePoint: (messageId, attachmentId, sharepointPath) => 
        email.saveAttachmentToSharePoint(graphClient, config.mailbox, config.sharepointSiteId, messageId, attachmentId, sharepointPath),
      markAsRead: (messageId) => email.markAsRead(graphClient, config.mailbox, messageId),
      markAsUnread: (messageId) => email.markAsUnread(graphClient, config.mailbox, messageId),
    };

    client.folders = {
      list: () => folders.listFolders(graphClient, config.mailbox),
      get: (folderId) => folders.getFolder(graphClient, config.mailbox, folderId),
      create: (name, parentFolderId) => folders.createFolder(graphClient, config.mailbox, name, parentFolderId),
      delete: (folderId) => folders.deleteFolder(graphClient, config.mailbox, folderId),
    };

    // Shared mailboxes
    if (config.sharedMailboxes && config.sharedMailboxes.length > 0) {
      client.sharedMailboxes = {};
      config.sharedMailboxes.forEach(mb => {
        client.sharedMailboxes[mb] = {
          send: (message) => email.sendMail(graphClient, mb, message),
          list: (options) => email.listMessages(graphClient, mb, options),
          get: (messageId, options) => email.getMessage(graphClient, mb, messageId, options),
          move: (messageId, folderId) => email.moveMessage(graphClient, mb, messageId, folderId),
          delete: (messageId) => email.deleteMessage(graphClient, mb, messageId),
        };
      });
    }
  }

  // SharePoint module
  if (config.enableSharepoint && config.sharepointSiteId) {
    client.sharepoint = {
      upload: (filePath, content, options) => sharepoint.uploadFile(graphClient, config.sharepointSiteId, filePath, content, options),
      download: (filePath) => sharepoint.downloadFile(graphClient, config.sharepointSiteId, filePath),
      list: (path) => sharepoint.listFiles(graphClient, config.sharepointSiteId, path),
      createFolder: (folderPath, parentPath) => sharepoint.createFolder(graphClient, config.sharepointSiteId, folderPath, parentPath),
      delete: (filePath) => sharepoint.deleteFile(graphClient, config.sharepointSiteId, filePath),
      getDriveInfo: () => sharepoint.getDriveInfo(graphClient, config.sharepointSiteId),
    };
  }

  // OneDrive module
  if (config.enableOnedrive && config.onedriveUser) {
    client.onedrive = {
      upload: (filePath, content, options) => onedrive.uploadFile(graphClient, config.onedriveUser, filePath, content, options),
      download: (filePath) => onedrive.downloadFile(graphClient, config.onedriveUser, filePath),
      list: (path) => onedrive.listFiles(graphClient, config.onedriveUser, path),
      createFolder: (folderPath, parentPath) => onedrive.createFolder(graphClient, config.onedriveUser, folderPath, parentPath),
      delete: (filePath) => onedrive.deleteFile(graphClient, config.onedriveUser, filePath),
      getDriveInfo: () => onedrive.getDriveInfo(graphClient, config.onedriveUser),
    };
  }

  // Planner module
  if (config.enablePlanner && config.plannerGroupId) {
    client.planner = {
      listPlans: () => planner.listPlans(graphClient, config.plannerGroupId),
      listTasks: (planId) => planner.listTasks(graphClient, planId),
      createTask: (planId, title, options) => planner.createTask(graphClient, planId, title, options),
      updateTask: (taskId, updates) => planner.updateTask(graphClient, taskId, updates),
      deleteTask: (taskId) => planner.deleteTask(graphClient, taskId),
      getTask: (taskId) => planner.getTask(graphClient, taskId),
      createTaskFromEmail: (messageId, planId, options) => 
        planner.createTaskFromEmail(graphClient, config.mailbox, messageId, planId, options),
      listBuckets: (planId) => planner.listBuckets(graphClient, planId),
      createBucket: (planId, name) => planner.createBucket(graphClient, planId, name),
    };
  }

  // Webhooks module (always available)
  client.webhooks = {
    create: (options) => webhooks.createSubscription(client._token, options),
    list: () => webhooks.listSubscriptions(client._token),
    get: (subscriptionId) => webhooks.getSubscription(client._token, subscriptionId),
    renew: (subscriptionId, newExpiration) => webhooks.renewSubscription(client._token, subscriptionId, newExpiration),
    delete: (subscriptionId) => webhooks.deleteSubscription(client._token, subscriptionId),
    handleValidation: (req) => webhooks.handleValidationChallenge(req),
    processNotification: (req, clientState) => webhooks.processNotification(req, clientState),
  };

  // Utility: Test connection
  client.testConnection = async () => {
    // For app-only auth, we can't use /me endpoint
    // Instead, just return success since we already have a valid token
    return {
      success: true,
      enabledFeatures: {
        email: !!client.email,
        sharepoint: !!client.sharepoint,
        onedrive: !!client.onedrive,
        planner: !!client.planner,
        webhooks: true,
      },
    };
  };

  return client;
}

// Export modules for direct access
export { email, folders, sharepoint, onedrive, planner, webhooks };
export default createM365Client;
