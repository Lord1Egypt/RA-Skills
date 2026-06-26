/**
 * SharePoint - File Operations
 */

/**
 * Upload a file to SharePoint
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} siteId - SharePoint site ID
 * @param {string} filePath - Path in SharePoint (e.g., '/Documents/folder/file.pdf')
 * @param {Buffer|String} content - File content
 * @param {Object} [options] - Upload options
 * @param {string} [options.contentType] - MIME type
 * @param {string} [options.conflict='rename'] - Conflict behavior (rename|replace|fail)
 * @returns {Promise<Object>} Uploaded file metadata
 */
export async function uploadFile(graphClient, siteId, filePath, content, options = {}) {
  const { contentType = 'application/octet-stream', conflict = 'rename' } = options;

  // Convert string to buffer if needed
  const contentBuffer = typeof content === 'string' ? Buffer.from(content) : content;

  // Build endpoint for file upload
  // Format: /sites/{site-id}/drive/root:/path/to/file:/content
  const endpoint = `/sites/${siteId}/drive/root:${filePath}:/content`;

  const response = await graphClient.api(endpoint)
    .headers({
      'Content-Type': contentType,
      'Content-Length': contentBuffer.length,
    })
    .put(contentBuffer);

  return response;
}

/**
 * Download a file from SharePoint
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} siteId - SharePoint site ID
 * @param {string} filePath - Path in SharePoint
 * @returns {Promise<Buffer>} File content
 */
export async function downloadFile(graphClient, siteId, filePath) {
  const endpoint = `/sites/${siteId}/drive/root:${filePath}:/content`;
  
  const response = await graphClient.api(endpoint).get();
  return response; // Binary content
}

/**
 * List files in a SharePoint folder
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} siteId - SharePoint site ID
 * @param {string} [path='/'] - Folder path
 * @returns {Promise<Array>} List of files/folders
 */
export async function listFiles(graphClient, siteId, path = '/') {
  const endpoint = path === '/'
    ? `/sites/${siteId}/drive/root/children`
    : `/sites/${siteId}/drive/root:${path}:/children`;

  const response = await graphClient.api(endpoint).get();
  return response.value;
}

/**
 * Create a folder in SharePoint
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} siteId - SharePoint site ID
 * @param {string} folderPath - Folder name to create
 * @param {string} [parentPath='/'] - Parent folder path
 * @returns {Promise<Object>} Created folder metadata
 */
export async function createFolder(graphClient, siteId, folderPath, parentPath = '/') {
  const endpoint = parentPath === '/'
    ? `/sites/${siteId}/drive/root/children`
    : `/sites/${siteId}/drive/root:${parentPath}:/children`;

  return graphClient.api(endpoint).post({
    name: folderPath,
    folder: {},
    '@microsoft.graph.conflictBehavior': 'rename',
  });
}

/**
 * Delete a file or folder from SharePoint
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} siteId - SharePoint site ID
 * @param {string} filePath - Path in SharePoint
 * @returns {Promise<void>}
 */
export async function deleteFile(graphClient, siteId, filePath) {
  const item = await graphClient.api(`/sites/${siteId}/drive/root:${filePath}`).get();
  await graphClient.api(`/sites/${siteId}/drive/items/${item.id}`).delete();
}

/**
 * Get SharePoint drive info
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} siteId - SharePoint site ID
 * @returns {Promise<Object>} Drive information
 */
export async function getDriveInfo(graphClient, siteId) {
  const response = await graphClient.api(`/sites/${siteId}/drive`).get();
  return {
    id: response.id,
    name: response.name,
    driveType: response.driveType,
    owner: response.owner,
    quota: response.quota,
  };
}

/**
 * Get file metadata
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} siteId - SharePoint site ID
 * @param {string} filePath - Path in SharePoint
 * @returns {Promise<Object>} File metadata
 */
export async function getFileMetadata(graphClient, siteId, filePath) {
  const response = await graphClient.api(`/sites/${siteId}/drive/root:${filePath}`).get();
  return {
    id: response.id,
    name: response.name,
    size: response.size,
    createdDateTime: response.createdDateTime,
    lastModifiedDateTime: response.lastModifiedDateTime,
    webUrl: response.webUrl,
    downloadUrl: response['@microsoft.graph.downloadUrl'],
  };
}

/**
 * Search files in SharePoint
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} siteId - SharePoint site ID
 * @param {string} query - Search query
 * @param {number} [top=10] - Max results
 * @returns {Promise<Array>} Matching files
 */
export async function searchFiles(graphClient, siteId, query, top = 10) {
  const response = await graphClient.api(`/sites/${siteId}/drive/root/search(q='${query}')`)
    .query({ $top: top })
    .get();
  
  return response.value;
}
