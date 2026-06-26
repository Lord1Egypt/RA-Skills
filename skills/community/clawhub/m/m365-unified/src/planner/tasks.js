/**
 * Microsoft Planner - Task Operations
 */

/**
 * List all plans in a group
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} groupId - M365 Group ID
 * @returns {Promise<Array>} List of plans
 */
export async function listPlans(graphClient, groupId) {
  const response = await graphClient.api(`/groups/${groupId}/planner/plans`).get();
  return response.value;
}

/**
 * List tasks in a plan
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} planId - Planner Plan ID
 * @returns {Promise<Array>} List of tasks
 */
export async function listTasks(graphClient, planId) {
  const response = await graphClient.api(`/planner/plans/${planId}/tasks`).get();
  return response.value;
}

/**
 * Create a new task
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} planId - Planner Plan ID
 * @param {string} title - Task title
 * @param {Object} [options] - Additional options
 * @param {string} [options.bucketId] - Bucket ID
 * @param {number} [options.priority=5] - Priority (1-9, 1=highest)
 * @param {number} [options.percentComplete=0] - Percent complete (0-100)
 * @param {string} [options.startDateTime] - Start date (ISO 8601)
 * @param {string} [options.dueDateTime] - Due date (ISO 8601)
 * @param {string} [options.assignee] - User ID to assign task to
 * @param {string} [options.description] - Task description
 * @returns {Promise<Object>} Created task
 */
export async function createTask(graphClient, planId, title, options = {}) {
  const {
    bucketId,
    priority = 5,
    percentComplete = 0,
    startDateTime,
    dueDateTime,
    assignee,
    description,
  } = options;

  const task = {
    planId,
    title,
    priority,
    percentComplete,
    ...(bucketId && { bucketId }),
    ...(startDateTime && { startDateTime }),
    ...(dueDateTime && { dueDateTime }),
  };

  const createdTask = await graphClient.api('/planner/tasks').post(task);

  // Add description if provided (requires separate API call)
  if (description) {
    await graphClient.api(`/planner/tasks/${createdTask.id}/details`).patch({
      description,
    });
  }

  // Assign to user if provided
  if (assignee) {
    const assignments = {};
    assignments[assignee] = {
      '@odata.type': '#microsoft.graph.plannerAssignment',
      assignedDateTime: new Date().toISOString(),
      orderHint: ' !',
      assignedBy: {
        user: {
          displayName: 'System',
          id: assignee,
        },
      },
    };

    await graphClient.api(`/planner/tasks/${createdTask.id}`)
      .patch({ assignments });
  }

  return createdTask;
}

/**
 * Update a task
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} taskId - Task ID
 * @param {Object} updates - Fields to update
 * @returns {Promise<Object>} Updated task
 */
export async function updateTask(graphClient, taskId, updates) {
  // Planner requires ETag for updates (optimistic concurrency)
  const currentTask = await getTask(graphClient, taskId);
  
  return graphClient.api(`/planner/tasks/${taskId}`)
    .headers({ 'If-Match': currentTask['@odata.etag'] })
    .patch(updates);
}

/**
 * Delete a task
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} taskId - Task ID
 * @returns {Promise<void>}
 */
export async function deleteTask(graphClient, taskId) {
  return graphClient.api(`/planner/tasks/${taskId}`).delete();
}

/**
 * Get a specific task
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} taskId - Task ID
 * @returns {Promise<Object>} Task object
 */
export async function getTask(graphClient, taskId) {
  return graphClient.api(`/planner/tasks/${taskId}`).get();
}

/**
 * Create a task from an email
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} mailbox - Mailbox email address
 * @param {string} messageId - Message ID
 * @param {string} planId - Planner Plan ID
 * @param {Object} [options] - Additional options
 * @param {string} [options.bucketId] - Bucket ID
 * @param {string} [options.assignee] - User ID to assign task to
 * @returns {Promise<Object>} Created task with email reference
 */
export async function createTaskFromEmail(graphClient, mailbox, messageId, planId, options = {}) {
  // Get email details
  const email = await graphClient.api(`/users/${mailbox}/messages/${messageId}`)
    .query({ $select: 'id,subject,from,receivedDateTime,bodyPreview,webLink' })
    .get();
  
  // Create task with email subject as title
  const description = `
**From:** ${email.from?.emailAddress?.name || email.from?.emailAddress?.address}
**Received:** ${new Date(email.receivedDateTime).toLocaleString()}
**Preview:** ${email.bodyPreview?.substring(0, 500) || 'No preview available'}

---
[View Original Email](${email.webLink})
  `.trim();

  const task = await createTask(graphClient, planId, email.subject, {
    ...options,
    description,
  });

  return {
    task,
    email: {
      id: messageId,
      subject: email.subject,
      from: email.from?.emailAddress?.address,
      receivedDateTime: email.receivedDateTime,
      webLink: email.webLink,
    },
  };
}

/**
 * List buckets in a plan
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} planId - Planner Plan ID
 * @returns {Promise<Array>} List of buckets
 */
export async function listBuckets(graphClient, planId) {
  const response = await graphClient.api(`/planner/plans/${planId}/buckets`).get();
  return response.value;
}

/**
 * Create a new bucket
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} planId - Planner Plan ID
 * @param {string} name - Bucket name
 * @returns {Promise<Object>} Created bucket
 */
export async function createBucket(graphClient, planId, name) {
  return graphClient.api('/planner/buckets').post({
    name,
    planId,
    orderHint: ' !',
  });
}

/**
 * Get task details (description, checklist, references)
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} taskId - Task ID
 * @returns {Promise<Object>} Task details
 */
export async function getTaskDetails(graphClient, taskId) {
  return graphClient.api(`/planner/tasks/${taskId}/details`).get();
}

/**
 * Update task details
 * 
 * @param {Client} graphClient - Microsoft Graph client
 * @param {string} taskId - Task ID
 * @param {Object} details - Details to update
 * @returns {Promise<Object>} Updated details
 */
export async function updateTaskDetails(graphClient, taskId, details) {
  const currentDetails = await getTaskDetails(graphClient, taskId);
  
  return graphClient.api(`/planner/tasks/${taskId}/details`)
    .headers({ 'If-Match': currentDetails['@odata.etag'] })
    .patch(details);
}
