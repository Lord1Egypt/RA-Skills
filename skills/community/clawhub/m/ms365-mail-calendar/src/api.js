// ms365/src/api.js
const { getAccessToken } = require('./auth');
const { normalizeAccount } = require('./config');

const GRAPH = 'https://graph.microsoft.com/v1.0';
let currentAccount = 'default';

function setAccount(a) { currentAccount = normalizeAccount(a); }

async function graph(endpoint, method = 'GET', body = null) {
  const token = await getAccessToken(currentAccount);
  const url = endpoint.startsWith('http') ? endpoint : `${GRAPH}${endpoint}`;
  const opts = { method, headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' } };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(url, opts);
  if (!res.ok) throw new Error(`Graph API ${res.status}: ${await res.text()}`);
  if (res.status === 204 || res.status === 202) return null;
  return res.json();
}

// === EMAIL ===
async function getEmails(top = 10) {
  const data = await graph(`/me/messages?$top=${top}&$orderby=receivedDateTime desc&$select=id,subject,from,receivedDateTime,isRead,bodyPreview`);
  return data?.value || [];
}

async function getUnreadEmails(top = 10) {
  const data = await graph(`/me/messages?$filter=isRead eq false&$top=${top}&$orderby=receivedDateTime desc&$select=id,subject,from,receivedDateTime,bodyPreview`);
  return data?.value || [];
}

async function readEmail(id) {
  const msg = await graph(`/me/messages/${id}?$select=id,subject,from,toRecipients,receivedDateTime,body,isRead,hasAttachments`);
  if (msg.hasAttachments) {
    const att = await graph(`/me/messages/${id}/attachments?$select=id,name,contentType,size,isInline`);
    msg.attachments = (att?.value || []).filter(a => !a.isInline);
  }
  return msg;
}

async function sendEmail(to, subject, body, cc = null) {
  const message = {
    subject,
    body: { contentType: 'Text', content: body },
    toRecipients: to.split(',').map(e => ({ emailAddress: { address: e.trim() } })),
  };
  if (cc) message.ccRecipients = cc.split(',').map(e => ({ emailAddress: { address: e.trim() } }));
  return graph('/me/sendMail', 'POST', { message });
}

async function searchEmails(query, top = 10) {
  const data = await graph(`/me/messages?$search="${encodeURIComponent(query)}"&$top=${top}&$select=id,subject,from,receivedDateTime,isRead,bodyPreview`);
  return data?.value || [];
}

// === CALENDAR ===
async function getEvents(startDate, endDate) {
  const start = startDate || new Date().toISOString().split('T')[0] + 'T00:00:00Z';
  const end = endDate || new Date().toISOString().split('T')[0] + 'T23:59:59Z';
  const data = await graph(`/me/calendarView?startDateTime=${start}&endDateTime=${end}&$orderby=start/dateTime&$select=id,subject,start,end,location,organizer,isAllDay`);
  return data?.value || [];
}

async function createEvent(subject, start, end, attendees = [], body = '') {
  const event = {
    subject,
    start: { dateTime: start, timeZone: 'Europe/Kyiv' },
    end: { dateTime: end, timeZone: 'Europe/Kyiv' },
    body: { contentType: 'Text', content: body },
  };
  if (attendees.length) {
    event.attendees = attendees.map(e => ({ emailAddress: { address: e }, type: 'required' }));
  }
  return graph('/me/events', 'POST', event);
}

async function deleteEvent(id) {
  return graph(`/me/events/${id}`, 'DELETE');
}

// === USER ===
async function getMe() {
  return graph('/me?$select=displayName,mail,userPrincipalName');
}

module.exports = { setAccount, getEmails, getUnreadEmails, readEmail, sendEmail, searchEmails, getEvents, createEvent, deleteEvent, getMe };
