const { httpRequest, getBaseUrl } = require('../utils/http');
const { getOrStartServer } = require('../utils/server');

async function querySessions() {
  const { port, close } = await getOrStartServer();
  const url = `${getBaseUrl('127.0.0.1', port)}/session`;
  const sessions = await httpRequest(url, { method: 'GET' });
  close();

  return {
    action: 'query',
    sessions: sessions.map(s => ({
      id: s.id,
      title: s.title,
      directory: s.directory,
      created: s.time?.created,
      updated: s.time?.updated
    }))
  };
}

async function createSession(taskDescription) {
  const { port, close } = await getOrStartServer();
  
  const url = `${getBaseUrl('127.0.0.1', port)}/session`;
  const body = JSON.stringify({ title: taskDescription.substring(0, 50) });
  
  const session = await httpRequest(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body
  });

  close();

  return {
    success: true,
    sessionId: session.id,
    directory: session.directory,
    baseUrl: getBaseUrl('127.0.0.1', port),
    message: "Session created. Use continue to execute task."
  };
}

module.exports = {
  querySessions,
  createSession
};