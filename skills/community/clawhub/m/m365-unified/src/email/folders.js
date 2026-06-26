/**
 * Exchange Online - Folder Operations
 */

/**
 * List all mail folders
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @returns {Promise<Array>} List of folders
 */
export async function listFolders(graphClient, mailbox) {
  const response = await graphClient.api(`/users/${mailbox}/mailFolders`).get();
  return response.value;
}

/**
 * Get a specific folder
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @param {string} folderId - Folder ID
 * @returns {Promise<Object>} Folder object
 */
export async function getFolder(graphClient, mailbox, folderId) {
  return graphClient.api(`/users/${mailbox}/mailFolders/${folderId}`).get();
}

/**
 * Create a new folder
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @param {string} name - Folder name
 * @param {string} [parentFolderId] - Parent folder ID (optional, creates in root if omitted)
 * @returns {Promise<Object>} Created folder
 */
export async function createFolder(graphClient, mailbox, name, parentFolderId = null) {
  const endpoint = parentFolderId
    ? `/users/${mailbox}/mailFolders/${parentFolderId}/childFolders`
    : `/users/${mailbox}/mailFolders`;

  return graphClient.api(endpoint).post({ displayName: name });
}

/**
 * Delete a folder
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @param {string} folderId - Folder ID
 * @returns {Promise<void>}
 */
export async function deleteFolder(graphClient, mailbox, folderId) {
  return graphClient.api(`/users/${mailbox}/mailFolders/${folderId}`).delete();
}

/**
 * Get folder by well-known name
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @param {string} name - Well-known name (inbox, sentitems, drafts, deleteditems, junkemail, archive)
 * @returns {Promise<Object>} Folder object
 */
export async function getWellKnownFolder(graphClient, mailbox, name) {
  const response = await graphClient.api(`/users/${mailbox}/mailFolders/${name}`).get();
  return response;
}

/**
 * Get folder statistics (item counts)
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @param {string} folderId - Folder ID
 * @returns {Promise<Object>} Folder statistics
 */
export async function getFolderStats(graphClient, mailbox, folderId) {
  const response = await graphClient.api(`/users/${mailbox}/mailFolders/${folderId}`)
    .query({ $select: 'displayName,totalItemCount,unreadItemCount,childFolderCount' })
    .get();
  
  return {
    name: response.displayName,
    totalItems: response.totalItemCount,
    unreadItems: response.unreadItemCount,
    childFolders: response.childFolderCount,
  };
}
