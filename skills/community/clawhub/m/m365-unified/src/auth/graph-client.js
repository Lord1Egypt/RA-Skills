/**
 * Microsoft Graph Client - Authentication
 * 
 * OAuth2 client credentials flow (app-only authentication).
 * Compatible with existing m365-planner skill.
 */

import axios from 'axios';

/**
 * Get OAuth2 access token from Microsoft Identity Platform
 * 
 * @param {Object} config - Configuration
 * @param {string} config.tenantId - Azure AD Tenant ID
 * @param {string} config.clientId - App Registration Client ID
 * @param {string} config.clientSecret - App Registration Client Secret
 * @returns {Promise<string>} Access token
 */
export async function getAccessToken(config) {
  const { tenantId, clientId, clientSecret } = config;

  if (!tenantId || !clientId || !clientSecret) {
    throw new Error('Missing required credentials: tenantId, clientId, clientSecret');
  }

  const tokenUrl = `https://login.microsoftonline.com/${tenantId}/oauth2/v2.0/token`;
  
  const params = new URLSearchParams();
  params.append('grant_type', 'client_credentials');
  params.append('client_id', clientId);
  params.append('client_secret', clientSecret);
  params.append('scope', 'https://graph.microsoft.com/.default');

  try {
    const response = await axios.post(tokenUrl, params, {
      headers: { 
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
      },
    });

    return response.data.access_token;
  } catch (error) {
    if (error.response) {
      const { status, data } = error.response;
      
      if (status === 401) {
        throw new Error('Authentication failed: Invalid client secret or tenant ID');
      } else if (status === 403) {
        throw new Error('Permission denied: App registration lacks required permissions');
      } else if (status === 404) {
        throw new Error('Tenant not found: Check tenant ID');
      } else {
        throw new Error(`Azure AD error (${status}): ${data.error_description || data.error}`);
      }
    } else {
      throw error;
    }
  }
}

/**
 * Validate credentials without making API calls
 * 
 * @param {Object} config - Configuration
 * @returns {Object} Validation result
 */
export function validateCredentials(config) {
  const errors = [];
  
  if (!config.tenantId) errors.push('Missing tenantId');
  if (!config.clientId) errors.push('Missing clientId');
  if (!config.clientSecret) errors.push('Missing clientSecret');
  
  // Basic format validation
  if (config.tenantId && !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(config.tenantId)) {
    errors.push('Invalid tenantId format (should be UUID)');
  }
  
  if (config.clientId && !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(config.clientId)) {
    errors.push('Invalid clientId format (should be UUID)');
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Decode JWT token to inspect claims and permissions
 * 
 * @param {string} token - JWT access token
 * @returns {Object} Decoded token payload
 */
export function decodeToken(token) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64).split('').map(c => 
        '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
      ).join('')
    );
    return JSON.parse(jsonPayload);
  } catch (error) {
    throw new Error('Failed to decode token: ' + error.message);
  }
}

/**
 * Check if token is expired or about to expire
 * 
 * @param {string} token - JWT access token
 * @param {number} bufferSeconds - Seconds before expiration to consider expired
 * @returns {Object} Expiration info
 */
export function checkTokenExpiration(token, bufferSeconds = 300) {
  const payload = decodeToken(token);
  const now = Math.floor(Date.now() / 1000);
  const exp = payload.exp;
  const iat = payload.iat;
  
  return {
    expired: now >= exp,
    expiringSoon: now >= (exp - bufferSeconds),
    expiresAt: new Date(exp * 1000).toISOString(),
    issuedAt: new Date(iat * 1000).toISOString(),
    secondsUntilExpiration: exp - now,
  };
}
