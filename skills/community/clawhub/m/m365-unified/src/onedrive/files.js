/**
 * OneDrive - File Operations
 */

/**
 * Upload a file to OneDrive
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} user - User email or 'me' for current user
 * @param {string} filePath - Path in OneDrive (e.g., '/Documents/folder/file.pdf')
 * @param {Buffer|String} content - File content
 * @param {Object} [options] - Upload options
 * @param {string} [options.contentType] - MIME type
 * @param {string} [options.conflict='rename'] - Conflict behavior (rename|replace|fail)
 * @returns {Promise<Object>} Uploaded file metadata
 */
export async function uploadFile(graphClient, user, filePath, content, options = {}) {
  const { contentType = 'application/octet-stream', conflict = 'rename' } = options;

  // Convert string to buffer if needed
  const contentBuffer = typeof content === 'string' ? Buffer.from(content) : content;

  // Build endpoint for file upload
  const endpoint = user === 'me'
    ? `/me/drive/root:${filePath}:/content`
    : `/users/${user}/drive/root:${filePath}:/content`;

  const response = await graphClient.api(endpoint)
    .headers({
      'Content-Type': contentType,
      'Content-Length': contentBuffer.length,
    })
    .put(contentBuffer);

  return response;
}

/**
 * Download a file from OneDrive
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} user - User email or 'me' for current user
 * @param {string} filePath - Path in OneDrive
 * @returns {Promise<Buffer>} File content
 */
export async function downloadFile(graphClient, user, filePath) {
  const endpoint = user === 'me'
    ? `/me/drive/root:${filePath}:/content`
    : `/users/${user}/drive/root:${filePath}:/content`;
  
  const response = await graphClient.api(endpoint).get();
  return response; // Binary content
}

/**
 * List files in a OneDrive folder
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} user - User email or 'me' for current user
 * @param {string} [path='/'] - Folder path
 * @returns {Promise<Array>} List of files/folders
 */
export async function listFiles(graphClient, user, path = '/') {
  const endpoint = path === '/'
    ? (user === 'me' ? '/me/drive/root/children' : `/users/${user}/drive/root/children`)
    : (user === 'me' 
        ? `/me/drive/root:${path}:/children`
        : `/users/${user}/drive/root:${path}:/children`);

  const response = await graphClient.api(endpoint).get();
  return response.value;
}

/**
 * Create a folder in OneDrive
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} user - User email or 'me' for current user
 * @param {string} folderPath - Folder name to create
 * @param {string} [parentPath='/'] - Parent folder path
 * @returns {Promise<Object>} Created folder metadata
 */
export async function createFolder(graphClient, user, folderPath, parentPath = '/') {
  const endpoint = parentPath === '/'
    ? (user === 'me' ? '/me/drive/root/children' : `/users/${user}/drive/root/children`)
    : (user === 'me'
        ? `/me/drive/root:${parentPath}:/children`
        : `/users/${user}/drive/root:${parentPath}:/children`);

  return graphClient.api(endpoint).post({
    name: folderPath,
    folder: {},
    '@microsoft.graph.conflictBehavior': 'rename',
  });
}

/**
 * Delete a file or folder from OneDrive
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} user - User email or 'me' for current user
 * @param {string} filePath - Path in OneDrive
 * @returns {Promise<void>}
 */
export async function deleteFile(graphClient, user, filePath) {
  const endpoint = user === 'me'
    ? `/me/drive/root:${filePath}`
    : `/users/${user}/drive/root:${filePath}`;
  
  const item = await graphClient.api(endpoint).get();
  await graphClient.api(`/me/drive/items/${item.id}`).delete();
}

/**
 * Get OneDrive drive info
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} user - User email or 'me' for current user
 * @returns {Promise<Object>} Drive information
 */
export async function getDriveInfo(graphClient, user) {
  const endpoint = user === 'me' ? '/me/drive' : `/users/${user}/drive`;
  
  const response = await graphClient.api(endpoint).get();
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
 * @param {string} user - User email or 'me' for current user
 * @param {string} filePath - Path in OneDrive
 * @returns {Promise<Object>} File metadata
 */
export async function getFileMetadata(graphClient, user, filePath) {
  const endpoint = user === 'me'
    ? `/me/drive/root:${filePath}`
    : `/users/${user}/drive/root:${filePath}`;
  
  const response = await graphClient.api(endpoint).get();
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
 * Search files in OneDrive
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} user - User email or 'me' for current user
 * @param {string} query - Search query
 * @param {number} [top=10] - Max results
 * @returns {Promise<Array>} Matching files
 */
export async function searchFiles(graphClient, user, query, top = 10) {
  const endpoint = user === 'me'
    ? `/me/drive/root/search(q='${query}')`
    : `/users/${user}/drive/root/search(q='${query}')`;
  
  const response = await graphClient.api(endpoint)
    .query({ $top: top })
    .get();
  
  return response.value;
}
