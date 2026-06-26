/**
 * Webhook Subscriptions - Microsoft Graph Change Notifications
 * 
 * Instead of polling with cron jobs, Microsoft Graph sends HTTP POST
 * requests to your webhook URL when resources change.
 */

import axios from 'axios';

/**
 * Create a new webhook subscription
 * @param {string} accessToken - OAuth2 access token
 * @param {Object} options - Subscription options
 * @param {string} options.resource - Resource to monitor (e.g., 'users/user@domain.com/messages')
 * @param {string} options.changeType - Type of changes (created, updated, deleted)
 * @param {string} options.notificationUrl - Your webhook endpoint URL
 * @param {string} options.expirationDateTime - ISO 8601 expiration date
 * @param {string} [options.clientState] - Secret validation string
 * @returns {Promise<Object>} Created subscription
 */
export async function createSubscription(accessToken, options) {
  const {
    resource,
    changeType,
    notificationUrl,
    expirationDateTime,
    clientState,
  } = options;

  const requestBody = {
    changeType,
    notificationUrl,
    resource,
    expirationDateTime,
    ...(clientState && { clientState }),
  };

  const response = await axios.post(
    'https://graph.microsoft.com/v1.0/subscriptions',
    requestBody,
    {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
    }
  );

  return response.data;
}

/**
 * List all active subscriptions
 * @param {string} accessToken - OAuth2 access token
 * @returns {Promise<Array>} List of subscriptions
 */
export async function listSubscriptions(accessToken) {
  const response = await axios.get(
    'https://graph.microsoft.com/v1.0/subscriptions',
    {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      },
    }
  );

  return response.data.value;
}

/**
 * Get a specific subscription
 * @param {string} accessToken - OAuth2 access token
 * @param {string} subscriptionId - Subscription ID
 * @returns {Promise<Object>} Subscription details
 */
export async function getSubscription(accessToken, subscriptionId) {
  const response = await axios.get(
    `https://graph.microsoft.com/v1.0/subscriptions/${subscriptionId}`,
    {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      },
    }
  );

  return response.data;
}

/**
 * Renew a subscription (extend expiration)
 * @param {string} accessToken - OAuth2 access token
 * @param {string} subscriptionId - Subscription ID
 * @param {string} newExpirationDateTime - New ISO 8601 expiration date
 * @returns {Promise<Object>} Updated subscription
 */
export async function renewSubscription(accessToken, subscriptionId, newExpirationDateTime) {
  const response = await axios.patch(
    `https://graph.microsoft.com/v1.0/subscriptions/${subscriptionId}`,
    {
      expirationDateTime: newExpirationDateTime,
    },
    {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
    }
  );

  return response.data;
}

/**
 * Delete a subscription
 * @param {string} accessToken - OAuth2 access token
 * @param {string} subscriptionId - Subscription ID
 * @returns {Promise<void>}
 */
export async function deleteSubscription(accessToken, subscriptionId) {
  await axios.delete(
    `https://graph.microsoft.com/v1.0/subscriptions/${subscriptionId}`,
    {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      },
    }
  );
}

/**
 * Validate webhook notification (validation token challenge)
 * 
 * When you create a subscription, Microsoft Graph sends a validation
 * request with a validationToken query parameter. Your endpoint must
 * return this token as plain text (200 OK).
 * 
 * @param {Object} req - Express/request object
 * @returns {string|null} Validation token if present, null otherwise
 */
export function handleValidationChallenge(req) {
  const validationToken = req.query.validationToken;
  
  if (validationToken) {
    // Return token as plain text (not JSON!)
    return validationToken;
  }
  
  return null;
}

/**
 * Process webhook notification
 * 
 * @param {Object} req - Express/request object
 * @param {string} clientState - Your secret client state for validation
 * @returns {Object|null} Parsed notification or null if invalid
 */
export function processNotification(req, clientState) {
  const notification = req.body;
  
  // Parse notification first
  if (!notification.value || !Array.isArray(notification.value)) {
    return null;
  }

  // Validate client state from FIRST change (Microsoft sends it in each array item)
  if (clientState && notification.value.length > 0) {
    const firstChangeClientState = notification.value[0].clientState;
    if (firstChangeClientState !== clientState) {
      console.warn('⚠️  Webhook client state mismatch - possible spoofing attempt');
      console.warn(`   Expected: ${clientState}`);
      console.warn(`   Got: ${firstChangeClientState}`);
      return null;
    }
  }

  // Return parsed changes
  return {
    subscriptionId: notification.value[0]?.subscriptionId,
    changes: notification.value.map(change => ({
      changeType: change.changeType,
      resource: change.resource,
      resourceId: change.resourceData?.id,
      resourceType: change.resourceData?.['@odata.type'],
      receivedDateTime: new Date().toISOString(),
    })),
  };
}

/**
 * Get common resource paths for subscriptions
 */
export const ResourceTypes = {
  // Email
  MAIL_INBOX: 'users/{user-id}/mailFolders/inbox/messages',
  MAIL_ALL: 'users/{user-id}/messages',
  MAIL_SENT: 'users/{user-id}/mailFolders/sentitems/messages',
  
  // SharePoint
  SHAREPOINT_FILES: 'sites/{site-id}/drive/root',
  SHAREPOINT_FOLDER: 'sites/{site-id}/drive/items/{item-id}/children',
  
  // OneDrive
  ONEDRIVE_FILES: 'me/drive/root',
  ONEDRIVE_FOLDER: 'me/drive/items/{item-id}/children',
  
  // Planner
  PLANNER_TASKS: 'planner/plans/{plan-id}/tasks',
  PLANNER_TASK: 'planner/tasks/{task-id}',
};

/**
 * Get maximum subscription duration (days)
 * 
 * Microsoft Graph subscriptions expire after a maximum period:
 * - Mail, Calendar, Contacts: 3 days
 * - Files (SharePoint/OneDrive): 3 days
 * - Planner: 3 days
 * 
 * You must renew subscriptions before they expire!
 */
export const MAX_SUBSCRIPTION_DAYS = {
  mail: 3,
  files: 3,
  planner: 3,
  default: 3,
};

/**
 * Calculate expiration date for subscription
 * @param {number} days - Number of days (default: 3)
 * @returns {string} ISO 8601 expiration date
 */
export function calculateExpirationDate(days = 3) {
  const date = new Date();
  date.setDate(date.getDate() + days);
  return date.toISOString();
}
