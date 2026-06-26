#!/usr/bin/env node

const fs = require('fs');

const args = process.argv.slice(2);
const ELEMENT_KEY = 'element-6066-11e4-a52e-4f735466cecf';
const HINGE_BUNDLE_ID = 'co.hinge.mobile.ios';

function hasFlag(name) {
  return args.includes(name);
}

function getArg(name, fallback = '') {
  const index = args.indexOf(name);
  if (index === -1) return fallback;
  return args[index + 1] || fallback;
}

function serverUrl() {
  return getArg('--server', process.env.APPIUM_SERVER || 'http://127.0.0.1:4723');
}

function sessionId() {
  return getArg('--session-id', process.env.APPIUM_SESSION_ID || '');
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function request(method, pathname, body) {
  let response;
  try {
    response = await fetch(`${serverUrl()}${pathname}`, {
      method,
      headers: { 'content-type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined
    });
  } catch (error) {
    throw new Error(`Unable to reach Appium at ${serverUrl()}.`);
  }

  const text = await response.text();
  const parsed = text ? JSON.parse(text) : {};
  if (!response.ok) {
    throw new Error(parsed.value?.message || `HTTP ${response.status}`);
  }
  return parsed;
}

function parseElementId(result) {
  const value = result?.value || {};
  return value[ELEMENT_KEY] || value.ELEMENT || '';
}

function decodeXml(value) {
  return value
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'")
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>');
}

function parseAttributes(chunk) {
  const attributes = {};
  const regex = /([A-Za-z0-9_:-]+)="([^"]*)"/g;
  let match;
  while ((match = regex.exec(chunk)) !== null) {
    attributes[match[1]] = decodeXml(match[2]);
  }
  return attributes;
}

function parseElements(xml) {
  const elements = [];
  const regex = /<(XCUIElementType[A-Za-z]+)\s+([^>]*?)\/?>/g;
  let match;
  while ((match = regex.exec(xml)) !== null) {
    const tagName = match[1];
    const attributes = parseAttributes(match[2]);
    attributes.type = attributes.type || tagName;
    elements.push(attributes);
  }
  return elements;
}

function uniqueBy(items, keyFn) {
  const seen = new Set();
  const result = [];
  for (const item of items) {
    const key = keyFn(item);
    if (seen.has(key)) continue;
    seen.add(key);
    result.push(item);
  }
  return result;
}

function isVisible(element) {
  return element.visible === 'true';
}

function elementName(element) {
  return element.name || element.label || element.value || '';
}

function parsePrompt(label) {
  const prefix = 'Prompt: ';
  const separator = ', Answer: ';
  if (!label.startsWith(prefix)) {
    return { label };
  }

  const remainder = label.slice(prefix.length);
  const separatorIndex = remainder.indexOf(separator);
  if (separatorIndex === -1) {
    return { label, prompt: remainder };
  }

  return {
    label,
    prompt: remainder.slice(0, separatorIndex),
    answer: remainder.slice(separatorIndex + separator.length)
  };
}

function extractProfileName(elements) {
  const skipButton = elements.find((element) => isVisible(element) && /^Skip /.test(elementName(element)));
  if (skipButton) {
    return elementName(skipButton).replace(/^Skip /, '').trim();
  }

  const likeButton = elements.find((element) => isVisible(element) && /^Like /.test(elementName(element)));
  if (!likeButton) {
    const header = elements.find(
      (element) =>
        isVisible(element) &&
        element.type === 'XCUIElementTypeStaticText' &&
        /Header/.test(element.traits || '') &&
        numericValue(element.y) <= 220
    );
    if (header) {
      return elementName(header).trim();
    }

    const candidate = elements.find(
      (element) =>
        isVisible(element) &&
        element.type === 'XCUIElementTypeStaticText' &&
        numericValue(element.y) <= 220 &&
        /^[A-Za-z][A-Za-z .'-]{1,30}$/.test(elementName(element))
    );
    return candidate ? elementName(candidate).trim() : '';
  }

  const match = elementName(likeButton).match(/^Like\s+(.+?)'s\s+/);
  return match ? match[1] : '';
}

function normalizeTabName(name) {
  if (name.startsWith('Chats & Matches')) return 'chats';
  if (name.startsWith('Likes You')) return 'likes';
  if (name === 'Discover') return 'discover';
  if (name === 'Standouts') return 'standouts';
  if (name === 'Settings') return 'settings';
  return '';
}

function numericValue(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : 0;
}

function isSelected(element) {
  return /Selected/.test(element.traits || '') || element.value === '1';
}

function getVisibleElements(elements) {
  return elements.filter(isVisible);
}

function detectScreenType(visibleElements, currentTab) {
  const hasSendInterestButton = visibleElements.some(
    (element) =>
      element.type === 'XCUIElementTypeButton' &&
      /Send Like|Send Rose|Send like with message|Send a Rose with message/i.test(elementName(element))
  );

  if (
    visibleElements.some((element) => element.type === 'XCUIElementTypeButton' && elementName(element) === 'Edit') &&
    visibleElements.some((element) => element.type === 'XCUIElementTypeButton' && elementName(element) === 'View') &&
    visibleElements.some((element) => element.type === 'XCUIElementTypeButton' && elementName(element) === 'Cancel') &&
    visibleElements.some((element) => element.type === 'XCUIElementTypeButton' && elementName(element) === 'Done')
  ) {
    return 'self-profile-editor';
  }

  if (
    currentTab === 'standouts' &&
    visibleElements.some((element) => element.type === 'XCUIElementTypeButton' && /^Roses \(/.test(elementName(element))) &&
    visibleElements.some((element) => element.type === 'XCUIElementTypeCell' && element.accessible === 'true' && /,/.test(elementName(element)))
  ) {
    return 'standouts-carousel';
  }

  if (
    currentTab === 'likes' &&
    visibleElements.some((element) => element.type === 'XCUIElementTypeStaticText' && /No likes yet/i.test(elementName(element)))
  ) {
    return 'likes-empty';
  }

  if (
    visibleElements.some((element) => element.type === 'XCUIElementTypeStaticText' && /^Matches$/.test(elementName(element))) &&
    visibleElements.some((element) => element.type === 'XCUIElementTypeCell' && /^[A-Za-z]/.test(elementName(element)))
  ) {
    return 'chat-list';
  }

  if (
    visibleElements.some((element) => element.type === 'XCUIElementTypeButton' && elementName(element) === 'Chat') &&
    visibleElements.some((element) => element.type === 'XCUIElementTypeButton' && elementName(element) === 'Profile') &&
    visibleElements.some((element) => element.type === 'XCUIElementTypeTextView' && elementName(element) === 'Send a message')
  ) {
    const profileTab = visibleElements.find(
      (element) => element.type === 'XCUIElementTypeButton' && elementName(element) === 'Profile'
    );
    return profileTab && isSelected(profileTab) ? 'thread-profile' : 'chat-thread';
  }

  if (
    visibleElements.some(
      (element) =>
        (element.type === 'XCUIElementTypeTextField' || element.type === 'XCUIElementTypeTextView') &&
        (/Add a comment/i.test(elementName(element)) || Boolean(elementName(element) || element.value))
    ) &&
    (
      visibleElements.some((element) => element.type === 'XCUIElementTypeButton' && /Send Like|Send Rose/i.test(elementName(element))) ||
      visibleElements.some((element) => element.type === 'XCUIElementTypeButton' && elementName(element) === 'Done')
    )
  ) {
    return 'like-composer';
  }

  // Some Hinge like composers expose "Add a comment" as a button, not a text field.
  if (
    hasSendInterestButton &&
    visibleElements.some((element) => element.type === 'XCUIElementTypeButton' && /Add a comment/i.test(elementName(element))) &&
    visibleElements.some((element) => element.type === 'XCUIElementTypeButton' && elementName(element) === 'Cancel')
  ) {
    return 'like-composer';
  }

  if (
    visibleElements.some(
      (element) => element.type === 'XCUIElementTypeButton' && /,\s*Edit comment$/i.test(elementName(element))
    ) &&
    visibleElements.some((element) => element.type === 'XCUIElementTypeButton' && /Send like with message|Send a Rose with message/i.test(elementName(element)))
  ) {
    return 'like-composer';
  }

  if (
    visibleElements.some((element) => element.type === 'XCUIElementTypeButton' && /^Like /.test(elementName(element))) ||
    visibleElements.some((element) => element.type === 'XCUIElementTypeButton' && /^Skip /.test(elementName(element)))
  ) {
    return 'profile';
  }

  return 'unknown';
}

function parseStandoutCards(visibleElements) {
  return uniqueBy(
    visibleElements
      .filter((element) => element.type === 'XCUIElementTypeCell' && element.accessible === 'true' && /,/.test(elementName(element)))
      .map((element) => {
        const label = elementName(element);
        const parts = label.split(',');
        return {
          label,
          name: (parts.shift() || '').trim(),
          teaser: parts.join(',').trim()
        };
      }),
    (item) => item.label
  );
}

function buildStandoutsSnapshot(visibleElements) {
  const rosesButton = visibleElements.find(
    (element) => element.type === 'XCUIElementTypeButton' && /^Roses \(/.test(elementName(element))
  );
  const rosesLabel = rosesButton ? elementName(rosesButton) : '';
  const rosesMatch = rosesLabel.match(/\((\d+)\)/);

  return {
    rosesLabel,
    rosesRemaining: rosesMatch ? Number(rosesMatch[1]) : null,
    cards: parseStandoutCards(visibleElements)
  };
}

function buildLikesSnapshot(visibleElements) {
  const emptyHeading = visibleElements.find(
    (element) => element.type === 'XCUIElementTypeStaticText' && /No likes yet/i.test(elementName(element))
  );
  const ctas = uniqueBy(
    visibleElements
      .filter((element) => element.type === 'XCUIElementTypeButton')
      .map((element) => elementName(element))
      .filter(Boolean),
    (item) => item
  );

  return {
    empty: Boolean(emptyHeading),
    headline: emptyHeading ? elementName(emptyHeading) : '',
    ctas
  };
}

function parseSelfPromptLabel(label) {
  const match = label.match(/^Edit prompt \d+:\s*(.+?):\s*(.+)$/);
  if (!match) {
    return null;
  }
  return {
    label,
    prompt: match[1].trim(),
    answer: match[2].trim()
  };
}

function buildSelfProfileSnapshot(visibleElements) {
  const prompts = uniqueBy(
    visibleElements
      .filter((element) => element.type === 'XCUIElementTypeButton' && /^Edit prompt \d+:/.test(elementName(element)))
      .map((element) => parseSelfPromptLabel(elementName(element)))
      .filter(Boolean),
    (item) => item.label
  );

  const nameCandidate = visibleElements.find(
    (element) =>
      element.type === 'XCUIElementTypeStaticText' &&
      isVisible(element) &&
      numericValue(element.y) <= 220 &&
      /^[A-Za-z][A-Za-z .'-]{1,30}$/.test(elementName(element)) &&
      !['Edit', 'View', 'Cancel', 'Done'].includes(elementName(element))
  );

  return {
    name: nameCandidate ? elementName(nameCandidate) : '',
    prompts,
    editModeVisible: visibleElements.some((element) => element.type === 'XCUIElementTypeButton' && elementName(element) === 'Edit'),
    viewModeVisible: visibleElements.some((element) => element.type === 'XCUIElementTypeButton' && elementName(element) === 'View')
  };
}

function parseChatSections(visibleElements) {
  return visibleElements
    .filter((element) => element.type === 'XCUIElementTypeStaticText' && /^(Your turn|Their turn|Hidden) \(\d+\)$/.test(elementName(element)))
    .map((element) => ({
      label: elementName(element),
      y: numericValue(element.y)
    }))
    .sort((left, right) => left.y - right.y);
}

function sectionForY(sections, y) {
  let current = '';
  for (const section of sections) {
    if (y >= section.y) {
      current = section.label;
    }
  }
  return current;
}

function buildChatListSnapshot(visibleElements) {
  const sections = parseChatSections(visibleElements);
  const threads = visibleElements
    .filter((element) => element.type === 'XCUIElementTypeCell' && element.accessible === 'true' && elementName(element))
    .map((element) => ({
      name: elementName(element),
      preview: element.value || '',
      section: sectionForY(sections, numericValue(element.y)),
      isStarter: /Start the chat with /.test(element.value || '')
    }));

  return {
    sections: sections.map((section) => section.label),
    threads
  };
}

function isDateStamp(text) {
  return /^(Mon|Tue|Wed|Thu|Fri|Sat|Sun),/.test(text);
}

function isSystemActionMessage(text) {
  return (
    /^Start the chat with /.test(text) ||
    /^You liked /.test(text) ||
    /^Liked your /.test(text) ||
    /^You sent a rose/i.test(text) ||
    /^Sent you a rose/i.test(text)
  );
}

function isThreadUiText(text) {
  if (!text) return true;
  if (['Chat', 'Profile', 'Back', 'Verified', 'More options', 'Send a message', 'Close', 'Today'].includes(text)) return true;
  if (text === 'Sent') return true;
  if (isDateStamp(text)) return true;
  if (/^\d{1,2}:\d{2}/.test(text)) return true;
  if (/^Get notifications from /.test(text)) return true;
  if (/^Timing is everything/.test(text)) return true;
  if (/^Enable for /.test(text)) return true;
  return false;
}

function inferMessageSide(item) {
  if (/^You /.test(item.text)) return 'you';
  if (/^Liked your /.test(item.text) || /^Start the chat with /.test(item.text)) return 'them';
  return item.x >= 95 ? 'you' : 'them';
}

function buildThreadSnapshot(visibleElements) {
  const title = visibleElements.find((element) => element.type === 'XCUIElementTypeStaticText' && /Header/.test(element.traits || ''));
  const titleText = title ? elementName(title) : '';
  const threadTabs = uniqueBy(
    visibleElements
      .filter((element) => element.type === 'XCUIElementTypeButton' && ['Chat', 'Profile'].includes(elementName(element)))
      .map((element) => ({
        label: elementName(element),
        selected: isSelected(element)
      })),
    (item) => item.label
  );
  const messages = uniqueBy(
    visibleElements
      .filter((element) => element.type === 'XCUIElementTypeStaticText')
      .map((element) => ({
        text: elementName(element),
        x: numericValue(element.x),
        y: numericValue(element.y)
      }))
      .filter((item) => !isThreadUiText(item.text) && item.text !== titleText)
      .sort((left, right) => right.y - left.y)
      .map((item) => ({
        text: item.text,
        side: inferMessageSide(item),
        isSystem: isSystemActionMessage(item.text)
      })),
    (item) => `${item.side}:${item.text}`
  );
  const composer = visibleElements.find((element) => element.type === 'XCUIElementTypeTextView' && elementName(element) === 'Send a message');
  const sendButtons = uniqueBy(
    visibleElements
      .filter((element) => element.type === 'XCUIElementTypeButton')
      .map((element) => elementName(element))
      .filter((name) => /send/i.test(name)),
    (item) => item
  );

  return {
    matchName: title ? elementName(title) : '',
    activeSubtab: threadTabs.find((tab) => tab.selected)?.label.toLowerCase() || '',
    subtabs: threadTabs,
    messages,
    lastSpeaker: messages[0]?.side || '',
    lastMessageText: messages[0]?.text || '',
    composerPlaceholder: composer ? elementName(composer) : '',
    sendButtons,
    canRecordVoice: visibleElements.some((element) => element.type === 'XCUIElementTypeButton' && elementName(element) === 'Record voice note')
  };
}

function buildLikeComposerSnapshot(visibleElements) {
  const textInput = visibleElements.find(
    (element) =>
      ['XCUIElementTypeTextField', 'XCUIElementTypeTextView'].includes(element.type) &&
      (elementName(element) || element.value)
  );
  const editButton = visibleElements.find(
    (element) => element.type === 'XCUIElementTypeButton' && /,\s*Edit comment$/i.test(elementName(element))
  );
  const sendButtons = uniqueBy(
    visibleElements
      .filter((element) => element.type === 'XCUIElementTypeButton')
      .map((element) => elementName(element))
      .filter((name) => /Send Like|Send Rose|Cancel|Send like with message|Send a Rose with message/i.test(name)),
    (item) => item
  );
  const componentLines = uniqueBy(
    visibleElements
      .filter((element) => element.type === 'XCUIElementTypeStaticText' && element.visible === 'true')
      .map((element) => ({
        text: elementName(element),
        y: numericValue(element.y),
        width: numericValue(element.width)
      }))
      .filter((item) => item.y >= 170 && item.y <= 620)
      .filter((item) => item.width >= 140)
      .map((item) => item.text)
      .filter(Boolean)
      .filter((text) => !/^(done|cancel|send like|send|add a comment)$/i.test(text))
      .filter((text) => !/,\s*Edit comment$/i.test(text))
      .filter((text) => text !== (textInput ? (elementName(textInput) || textInput.value || '') : '')),
    (item) => item
  ).slice(0, 4);
  const imageLabel =
    visibleElements.find(
      (element) =>
        element.type === 'XCUIElementTypeImage' &&
        element.visible === 'true' &&
        /'s (photo|video)/i.test(elementName(element))
    )?.name || '';

  return {
    commentText: textInput
      ? (elementName(textInput) || textInput.value || '')
      : (editButton ? elementName(editButton).replace(/,\s*Edit comment$/i, '').trim() : ''),
    sendButtons,
    componentLines,
    imageLabel
  };
}

function buildSnapshot(xml) {
  const elements = parseElements(xml);
  const application = elements.find((element) => element.type === 'XCUIElementTypeApplication') || {};
  const visibleElements = getVisibleElements(elements);
  const prompts = uniqueBy(
    visibleElements
      .filter((element) => elementName(element).startsWith('Prompt: '))
      .map((element) => parsePrompt(elementName(element))),
    (item) => item.label
  );
  const likeTargets = uniqueBy(
    visibleElements
      .filter((element) => element.type === 'XCUIElementTypeButton' && /^Like /.test(elementName(element)))
      .map((element) => elementName(element)),
    (item) => item
  );
  const tabs = uniqueBy(
    visibleElements
      .filter((element) => element.type === 'XCUIElementTypeButton')
      .map((element) => ({
        key: normalizeTabName(elementName(element)),
        label: elementName(element),
        selected: /Selected/.test(element.traits || '') || element.value === '1'
      }))
      .filter((item) => item.key),
    (item) => item.key
  );
  const currentTab = tabs.find((item) => item.selected)?.key || '';
  const filters = uniqueBy(
    visibleElements
      .filter((element) => element.type === 'XCUIElementTypeButton' && /filter options$/.test(elementName(element)))
      .map((element) => elementName(element)),
    (item) => item
  );
  const currentProfile = {
    name: extractProfileName(elements),
    skipButton: visibleElements.find((element) => element.type === 'XCUIElementTypeButton' && /^Skip /.test(elementName(element)))
      ? elementName(visibleElements.find((element) => element.type === 'XCUIElementTypeButton' && /^Skip /.test(elementName(element))))
      : '',
    moreOptionsAvailable: visibleElements.some((element) => element.type === 'XCUIElementTypeButton' && elementName(element) === 'More options'),
    undoAvailable: visibleElements.some((element) => element.type === 'XCUIElementTypeButton' && elementName(element) === 'Undo')
  };
  const statusBadges = uniqueBy(
    visibleElements
      .filter((element) => element.type === 'XCUIElementTypeStaticText')
      .map((element) => elementName(element))
      .filter((text) => ['Active today', 'Active now', 'New here'].includes(text)),
    (item) => item
  );
  const screenType = detectScreenType(visibleElements, currentTab);

  return {
    app: {
      name: application.name || '',
      bundleId: application.bundleId || ''
    },
    screenType,
    currentTab,
    currentProfile,
    prompts,
    likeTargets,
    filters,
    statusBadges,
    tabs,
    chats: screenType === 'chat-list' ? buildChatListSnapshot(visibleElements) : null,
    thread: ['chat-thread', 'thread-profile'].includes(screenType) ? buildThreadSnapshot(visibleElements) : null,
    likes: currentTab === 'likes' ? buildLikesSnapshot(visibleElements) : null,
    standouts: currentTab === 'standouts' ? buildStandoutsSnapshot(visibleElements) : null,
    selfProfile: screenType === 'self-profile-editor' ? buildSelfProfileSnapshot(visibleElements) : null,
    composer: screenType === 'like-composer' ? buildLikeComposerSnapshot(visibleElements) : null
  };
}

async function getSource() {
  if (!sessionId()) throw new Error('Missing session id');
  const result = await request('GET', `/session/${sessionId()}/source`);
  return result.value || '';
}

async function findElement(using, value) {
  const result = await request('POST', `/session/${sessionId()}/element`, { using, value });
  return parseElementId(result);
}

async function findElementWithRetry(using, value, options = {}) {
  const attempts = options.attempts || 5;
  const delayMs = options.delayMs || 400;

  for (let attempt = 0; attempt < attempts; attempt += 1) {
    try {
      return await findElement(using, value);
    } catch (error) {
      if (attempt === attempts - 1) {
        throw error;
      }
      await sleep(delayMs);
    }
  }

  throw new Error(`Unable to find element for ${using}: ${value}`);
}

async function tapElement(elementId) {
  return request('POST', `/session/${sessionId()}/element/${elementId}/click`, {});
}

async function tapByAccessibilityId(label) {
  const elementId = await findElement('accessibility id', label);
  await tapElement(elementId);
  return elementId;
}

async function tapByPredicate(predicate) {
  const elementId = await findElement('-ios predicate string', predicate);
  await tapElement(elementId);
  return elementId;
}

async function typeIntoElement(elementId, text) {
  await request('POST', `/session/${sessionId()}/element/${elementId}/value`, {
    text,
    value: Array.from(text)
  });
}

async function clearElement(elementId) {
  await request('POST', `/session/${sessionId()}/element/${elementId}/clear`, {});
}

async function activateHinge() {
  await request('POST', `/session/${sessionId()}/appium/device/activate_app`, { bundleId: HINGE_BUNDLE_ID });
}

async function screenshot(outPath) {
  const result = await request('GET', `/session/${sessionId()}/screenshot`);
  fs.writeFileSync(outPath, Buffer.from(result.value, 'base64'));
}

async function performSwipe(startX, startY, endX, endY, duration) {
  await request('POST', `/session/${sessionId()}/actions`, {
    actions: [
      {
        type: 'pointer',
        id: 'finger1',
        parameters: { pointerType: 'touch' },
        actions: [
          { type: 'pointerMove', duration: 0, x: startX, y: startY },
          { type: 'pointerDown', button: 0 },
          { type: 'pause', duration: 100 },
          { type: 'pointerMove', duration, x: endX, y: endY },
          { type: 'pointerUp', button: 0 }
        ]
      }
    ]
  });
  await request('DELETE', `/session/${sessionId()}/actions`);
}

async function performTap(x, y) {
  await request('POST', `/session/${sessionId()}/actions`, {
    actions: [
      {
        type: 'pointer',
        id: 'finger1',
        parameters: { pointerType: 'touch' },
        actions: [
          { type: 'pointerMove', duration: 0, x, y },
          { type: 'pointerDown', button: 0 },
          { type: 'pause', duration: 80 },
          { type: 'pointerUp', button: 0 }
        ]
      }
    ]
  });
  await request('DELETE', `/session/${sessionId()}/actions`);
}

async function scrollDirection(direction) {
  const xml = await getSource();
  const elements = parseElements(xml);
  const application = elements.find((element) => element.type === 'XCUIElementTypeApplication') || {};
  const width = Number(application.width || 390);
  const height = Number(application.height || 844);
  const midX = Math.round(width / 2);
  const downStart = Math.round(height * 0.72);
  const downEnd = Math.round(height * 0.34);
  const upStart = Math.round(height * 0.34);
  const upEnd = Math.round(height * 0.72);
  if (direction === 'down') {
    await performSwipe(midX, downStart, midX, downEnd, 450);
    return;
  }
  if (direction === 'up') {
    await performSwipe(midX, upStart, midX, upEnd, 450);
    return;
  }
  throw new Error(`Unsupported scroll direction: ${direction}`);
}

function tabLabelForKey(tab) {
  const normalized = normalizeTabKey(tab);
  const names = {
    discover: 'Discover',
    standouts: 'Standouts',
    likes: 'Likes You',
    chats: 'Chats & Matches',
    settings: 'Settings'
  };
  return names[normalized] || '';
}

function matchingTabElement(elements, tab) {
  const prefix = tabLabelForKey(tab);
  if (!prefix) {
    return null;
  }
  return elements.find(
    (element) =>
      element.type === 'XCUIElementTypeButton' &&
      element.name &&
      element.name.startsWith(prefix)
  );
}

async function loadUiTree() {
  const xml = await getSource();
  const elements = parseElements(xml);
  const application = elements.find((element) => element.type === 'XCUIElementTypeApplication') || {};
  return { xml, elements, application };
}

function normalizeTabKey(tab) {
  const raw = String(tab || '').trim().toLowerCase();
  if (['discover', 'home'].includes(raw)) return 'discover';
  if (['standouts', 'standout'].includes(raw)) return 'standouts';
  if (['likes', 'like'].includes(raw)) return 'likes';
  if (['chats', 'chat', 'matches', 'messages', 'inbox'].includes(raw)) return 'chats';
  if (['settings', 'profile', 'me'].includes(raw)) return 'settings';
  return raw;
}

function hasVisibleText(elements, pattern) {
  return elements.some(
    (element) =>
      element.visible === 'true' &&
      ['XCUIElementTypeStaticText', 'XCUIElementTypeButton', 'XCUIElementTypeOther'].includes(element.type) &&
      pattern.test(elementName(element))
  );
}

function findVisibleButton(elements, name) {
  return elements.find(
    (element) =>
      element.visible === 'true' &&
      element.type === 'XCUIElementTypeButton' &&
      elementName(element) === name
  );
}

function visibleButtonNames(elements) {
  return Array.from(
    new Set(
      elements
        .filter((element) => element.visible === 'true' && element.type === 'XCUIElementTypeButton')
        .map((element) => elementName(element))
        .filter(Boolean)
    )
  );
}

function hasPrimaryTabButtons(elements) {
  const tabPrefixes = ['Discover', 'Standouts', 'Likes You', 'Chats & Matches', 'Settings'];
  return elements.some(
    (element) =>
      element.visible === 'true' &&
      element.type === 'XCUIElementTypeButton' &&
      tabPrefixes.some((prefix) => elementName(element).startsWith(prefix))
  );
}

function hasPromotionSignals(elements) {
  const patterns = [
    /hingex/i,
    /upgrade/i,
    /premium/i,
    /boost/i,
    /superboost/i,
    /see who likes you/i,
    /stand out/i,
    /more likes/i,
    /unlimited likes/i,
    /weekly rose/i,
    /priority likes/i
  ];
  return patterns.some((pattern) => hasVisibleText(elements, pattern));
}

function pickOverlayDismissButtonLabel(elements, allowCancelFallback = false) {
  const names = visibleButtonNames(elements);
  if (!names.length) return '';

  const preferred = [
    /^Close$/i,
    /^Dismiss$/i,
    /^Not Now$/i,
    /^Maybe Later$/i,
    /^No Thanks!?$/i,
    /^No, thanks!?$/i,
    /^Skip$/i,
    /^Not now$/i,
    /^Maybe later$/i
  ];
  if (allowCancelFallback) {
    preferred.push(/^Cancel$/i);
  }

  for (const pattern of preferred) {
    const match = names.find((name) => pattern.test(name));
    if (match) return match;
  }

  return '';
}

async function dismissKnownOverlay(elements, application = {}) {
  const closeButton = findVisibleButton(elements, 'Close');
  if (
    closeButton &&
    (hasVisibleText(elements, /^Get notifications from /) ||
      hasVisibleText(elements, /Timing is everything/i))
  ) {
    await tapByAccessibilityId('Close');
    await sleep(350);
    return {
      dismissed: 'notifications-prompt'
    };
  }

  const hasTabs = hasPrimaryTabButtons(elements);
  const looksPromotional = hasPromotionSignals(elements);
  const dismissLabel = pickOverlayDismissButtonLabel(elements, !hasTabs || looksPromotional);

  if (dismissLabel && (!hasTabs || looksPromotional)) {
    await tapByAccessibilityId(dismissLabel);
    await sleep(350);
    return {
      dismissed: 'generic-modal',
      action: dismissLabel
    };
  }

  if (!hasTabs && looksPromotional) {
    const width = Number(application.width || 390);
    const x = Math.max(24, width - 28);
    const y = 60;
    await performTap(x, y);
    await sleep(300);
    return {
      dismissed: 'generic-modal-corner-tap',
      action: `tap(${x},${y})`
    };
  }

  return null;
}

async function dismissKnownOverlayIfPresent(maxAttempts = 3) {
  const actions = [];
  for (let attempt = 0; attempt < maxAttempts; attempt += 1) {
    const { elements, application } = await loadUiTree();
    const result = await dismissKnownOverlay(elements, application);
    if (!result) break;
    actions.push(result);
    await sleep(220);
  }
  if (!actions.length) {
    return { dismissed: false };
  }
  return {
    dismissed: true,
    actions
  };
}

async function escapeTabBlockingScreens(maxSteps = 3) {
  for (let step = 0; step < maxSteps; step += 1) {
    const snapshot = buildSnapshot(await getSource());
    if (!['chat-thread', 'thread-profile', 'self-profile-editor', 'like-composer'].includes(snapshot.screenType)) {
      return {
        escaped: step > 0,
        screenType: snapshot.screenType
      };
    }

    if (snapshot.screenType === 'self-profile-editor' || snapshot.screenType === 'like-composer') {
      await tapByAccessibilityId('Cancel');
      await sleep(350);
      continue;
    }

    try {
      await tapByAccessibilityId('Back');
      await sleep(350);
    } catch (error) {
      break;
    }
  }

  const finalSnapshot = buildSnapshot(await getSource());
  return {
    escaped: false,
    screenType: finalSnapshot.screenType
  };
}

async function revealTabBar(application) {
  const width = Number(application.width || 390);
  const height = Number(application.height || 844);
  const midX = Math.round(width / 2);
  const wakeY = Math.round(height * 0.58);

  await performTap(midX, wakeY);
  await sleep(250);
  // Hinge restores the bottom tab bar when the profile is nudged upward.
  await performSwipe(midX, Math.round(height * 0.34), midX, Math.round(height * 0.74), 220);
  await sleep(250);
}

async function openSelfProfileEditor() {
  const { application } = await loadUiTree();
  const width = Number(application.width || 390);
  const height = Number(application.height || 844);
  const x = Math.round(width / 2);
  const y = Math.round(height * 0.17);
  await performTap(x, y);
  await sleep(500);
  return { x, y };
}

async function openSelfProfileView() {
  await openSelfProfileEditor();
  const elementId = await findElementWithRetry('accessibility id', 'View', {
    attempts: 6,
    delayMs: 300
  });
  await tapElement(elementId);
  return { opened: 'View', elementId };
}

async function openFirstStandout() {
  const snapshot = buildSnapshot(await getSource());
  const firstCard = snapshot.standouts?.cards?.[0];
  if (!firstCard?.label) {
    throw new Error('No visible standout card found');
  }
  const elementId = await tapByAccessibilityId(firstCard.label);
  return { card: firstCard, elementId };
}

async function goTab(tab) {
  const normalizedTab = normalizeTabKey(tab);
  const knownTab = tabLabelForKey(normalizedTab);
  if (!knownTab) {
    throw new Error(`Unsupported tab: ${tab}`);
  }

  await dismissKnownOverlayIfPresent();
  await escapeTabBlockingScreens();

  let lastTree = null;
  for (let attempt = 0; attempt < 4; attempt += 1) {
    let { elements, application } = await loadUiTree();
    lastTree = { elements, application };
    let tabElement = matchingTabElement(elements, normalizedTab);

    if (!tabElement) {
      const dismissed = await dismissKnownOverlay(elements, application);
      if (dismissed) {
        continue;
      }
      await revealTabBar(application);
      ({ elements, application } = await loadUiTree());
      lastTree = { elements, application };
      tabElement = matchingTabElement(elements, normalizedTab);
    }

    if (!tabElement) {
      continue;
    }

    if (tabElement.visible === 'true') {
      await tapByAccessibilityId(elementName(tabElement));
      return { tab: normalizedTab, strategy: 'accessibility', target: elementName(tabElement) };
    }

    const width = Number(application.width || 390);
    const height = Number(application.height || 844);
    const centerX = Math.round(Number(tabElement.x || 0) + Number(tabElement.width || 0) / 2);
    const intendedY = Math.round(Number(tabElement.y || 0) + Number(tabElement.height || 0) / 2);
    const fallbackY = Math.min(height - 22, Math.max(height - 48, intendedY));
    const fallbackX = Math.max(24, Math.min(width - 24, centerX));
    await performTap(fallbackX, fallbackY);
    return { tab: normalizedTab, strategy: 'coordinate', x: fallbackX, y: fallbackY };
  }

  throw new Error(`Unable to reach tab: ${normalizedTab}`);
}

function profileFingerprint(snapshot) {
  return JSON.stringify({
    name: snapshot?.currentProfile?.name || '',
    prompts: (snapshot?.prompts || []).map((prompt) => `${prompt.prompt}:${prompt.answer}`),
    likeTargets: snapshot?.likeTargets || []
  });
}

async function waitForProfileChange(previousSnapshot, attempts = 6, delayMs = 500) {
  const previousFingerprint = profileFingerprint(previousSnapshot);
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    await sleep(delayMs);
    const nextSnapshot = buildSnapshot(await getSource());
    if (nextSnapshot.screenType !== 'profile') {
      return {
        advanced: true,
        snapshot: nextSnapshot
      };
    }
    if (profileFingerprint(nextSnapshot) !== previousFingerprint) {
      return {
        advanced: true,
        snapshot: nextSnapshot
      };
    }
  }

  return {
    advanced: false,
    snapshot: buildSnapshot(await getSource())
  };
}

function assertProfileAffinity(expectedName, snapshot, stage) {
  const expected = String(expectedName || '').trim().toLowerCase();
  const actual = String(snapshot?.currentProfile?.name || '').trim().toLowerCase();
  if (expected && actual && expected !== actual) {
    throw new Error(`Composer drifted from ${expectedName} to ${snapshot.currentProfile.name} during ${stage}`);
  }
}

async function tapSkipCoordinate(application, likeButton, variant = 'primary') {
  const width = Number(application.width || 390);
  const height = Number(application.height || 844);

  let targetX = Math.round(width * (variant === 'secondary' ? 0.1 : 0.18));
  let targetY = Math.round(height * 0.84);

  if (likeButton) {
    const likeCenterX = Math.round(numericValue(likeButton.x) + numericValue(likeButton.width) / 2);
    const likeCenterY = Math.round(numericValue(likeButton.y) + numericValue(likeButton.height) / 2);
    const leftMirror = width - likeCenterX;
    targetX =
      variant === 'secondary'
        ? Math.max(20, Math.min(Math.round(width * 0.3), Math.round(leftMirror * 0.72)))
        : Math.max(28, Math.min(Math.round(width * 0.42), leftMirror));
    targetY = variant === 'secondary' ? likeCenterY + 8 : likeCenterY;
  }

  await performTap(targetX, targetY);
  return {
    strategy: 'coordinate',
    x: targetX,
    y: targetY,
    variant
  };
}

async function skipCurrentProfile() {
  const { elements, application } = await loadUiTree();
  const snapshot = buildSnapshot(await getSource());
  if (snapshot.currentProfile.skipButton) {
    const elementId = await tapByAccessibilityId(snapshot.currentProfile.skipButton);
    const verification = await waitForProfileChange(snapshot);
    if (!verification.advanced) {
      throw new Error(`Skip did not advance profile ${snapshot.currentProfile.name || ''}`.trim());
    }
    return {
      skipped: snapshot.currentProfile.name,
      strategy: 'accessibility',
      elementId,
      advanced: true
    };
  }

  if (snapshot.screenType !== 'profile') {
    throw new Error('No visible skip button on the current Hinge screen');
  }

  const width = Number(application.width || 390);
  const height = Number(application.height || 844);
  const likeButton = elements.find(
    (element) =>
      element.visible === 'true' &&
      element.type === 'XCUIElementTypeButton' &&
      /^Like /.test(elementName(element))
  );

  const attempts = ['primary', 'secondary'];
  for (const variant of attempts) {
    const tapResult = await tapSkipCoordinate(application, likeButton, variant);
    const verification = await waitForProfileChange(snapshot);
    if (verification.advanced) {
      return {
        skipped: snapshot.currentProfile.name,
        ...tapResult,
        advanced: true
      };
    }
  }

  throw new Error(`Skip did not advance profile ${snapshot.currentProfile.name || ''}`.trim());
}

async function fillVisibleCommentComposer(comment) {
  const normalizedComment = String(comment ?? '');

  try {
    const editButtonId = await findElementWithRetry(
      '-ios predicate string',
      `type == 'XCUIElementTypeButton' AND name ENDSWITH 'Edit comment' AND visible == 1`,
      {
        attempts: 2,
        delayMs: 150
      }
    );
    await tapElement(editButtonId);
    await sleep(350);
  } catch (error) {
    // No collapsed edit button; the keyboard composer may already be open.
  }
  const textViewId = await findElementWithRetry(
    '-ios predicate string',
    `type == 'XCUIElementTypeTextView' AND visible == 1`,
    {
      attempts: 6,
      delayMs: 250
    }
  );
  try {
    await clearElement(textViewId);
    await sleep(150);
  } catch (error) {
    // Hinge's composer usually supports clear(), but keep typing as a fallback.
  }
  if (normalizedComment) {
    await typeIntoElement(textViewId, normalizedComment);
    await sleep(300);
  }

  return {
    comment: normalizedComment
  };
}

async function replaceOpenInterestComposerComment(comment) {
  const result = await fillVisibleCommentComposer(comment);
  return {
    ...result,
    replaced: true
  };
}

async function stageInterestWithComment(kind, comment, targetLabel) {
  const opened = await openInterestComposer(kind, targetLabel);
  await fillVisibleCommentComposer(comment);

  return {
    ...opened,
    comment,
    staged: true
  };
}

async function openInterestSheet(targetLabel) {
  const snapshot = buildSnapshot(await getSource());
  const target = targetLabel || snapshot.likeTargets.find((label) => /photo/i.test(label)) || snapshot.likeTargets[0];
  if (!target) {
    throw new Error('No visible like target found on the current Hinge screen');
  }

  await tapByAccessibilityId(target);
  await sleep(300);

  return {
    target
  };
}

async function openInterestComposer(kind, targetLabel) {
  const snapshot = buildSnapshot(await getSource());
  const target = targetLabel || snapshot.likeTargets.find((label) => /answer|photo/.test(label)) || snapshot.likeTargets[0];
  if (!target) {
    throw new Error('No visible like target found on the current Hinge screen');
  }

  await tapByAccessibilityId(target);
  await sleep(300);

  const addCommentElementId = await findElementWithRetry('accessibility id', 'Add a comment', {
    attempts: 6,
    delayMs: 300
  });
  await tapElement(addCommentElementId);
  await sleep(300);

  return {
    kind,
    target
  };
}

function sendButtonPatterns(kind) {
  if (kind === 'rose') {
    return [
      /send\s+a?\s*rose/i,
      /send/i
    ];
  }
  return [
    /send\s*like/i,
    /send/i
  ];
}

function pickVisibleSendButton(elements, application, kind) {
  const height = Number(application.height || 844);
  const width = Number(application.width || 390);
  const buttons = elements
    .filter((element) => element.visible === 'true' && element.type === 'XCUIElementTypeButton')
    .map((element) => ({
      ...element,
      labelText: elementName(element),
      xNum: numericValue(element.x),
      yNum: numericValue(element.y),
      widthNum: numericValue(element.width),
      heightNum: numericValue(element.height)
    }))
    .filter((element) => element.yNum >= height * 0.35)
    .filter(
      (element) =>
        !/^(done|cancel)$/i.test(element.labelText) &&
        !/record voice note/i.test(element.labelText) &&
        !/dictation/i.test(element.labelText) &&
        !/microphone/i.test(element.labelText)
    );

  for (const pattern of sendButtonPatterns(kind)) {
    const matched = buttons.find((button) => pattern.test(button.labelText));
    if (matched) return matched;
  }

  const largeCenteredButton = buttons.find((button) => {
    const centerX = button.xNum + button.widthNum / 2;
    return button.widthNum >= width * 0.42 && Math.abs(centerX - width / 2) <= width * 0.2;
  });
  if (largeCenteredButton) return largeCenteredButton;

  return buttons.sort((left, right) => (right.yNum + right.xNum) - (left.yNum + left.xNum))[0] || null;
}

async function tapResolvedButton(button) {
  if (!button) {
    throw new Error('No visible send button found');
  }

  const x = Math.round(button.xNum + button.widthNum / 2);
  const y = Math.round(button.yNum + button.heightNum / 2);

  if (button.labelText && !/send/i.test(button.labelText)) {
    try {
      await tapByAccessibilityId(button.labelText);
      return {
        strategy: 'accessibility',
        label: button.labelText
      };
    } catch (error) {
      // Fall through to coordinate tap.
    }
  }

  await performTap(x, y);
  return {
    strategy: 'coordinate',
    label: button.labelText || '',
    x,
    y
  };
}

async function composerStillVisible(kind) {
  const { elements, application } = await loadUiTree();
  const hasTextView = elements.some(
    (element) =>
      element.visible === 'true' &&
      ['XCUIElementTypeTextView', 'XCUIElementTypeTextField'].includes(element.type)
  );
  return hasTextView && Boolean(pickVisibleSendButton(elements, application, kind));
}

async function dismissKeyboardIfPresent() {
  try {
    const doneButtonId = await findElementWithRetry('accessibility id', 'Done', {
      attempts: 2,
      delayMs: 150
    });
    await tapElement(doneButtonId);
    await sleep(250);
    return { dismissed: true, strategy: 'done-button' };
  } catch (error) {
    return { dismissed: false, strategy: 'none' };
  }
}

async function dismissDictationPromptIfPresent() {
  try {
    const notNowButtonId = await findElementWithRetry('accessibility id', 'Not Now', {
      attempts: 2,
      delayMs: 150
    });
    await tapElement(notNowButtonId);
    await sleep(300);
    return { dismissed: true, strategy: 'not-now' };
  } catch (error) {
    return { dismissed: false, strategy: 'none' };
  }
}

async function tapSendComposerButton(kind) {
  await dismissDictationPromptIfPresent();
  await dismissKeyboardIfPresent();
  const { elements, application } = await loadUiTree();
  const button = pickVisibleSendButton(elements, application, kind);
  return tapResolvedButton(button);
}

async function sendInterestWithComment(kind, comment, targetLabel) {
  const beforeSnapshot = buildSnapshot(await getSource());
  const opened = await openInterestComposer(kind, targetLabel);
  const expectedProfileName = beforeSnapshot.currentProfile?.name || '';
  assertProfileAffinity(expectedProfileName, buildSnapshot(await getSource()), 'open');
  await fillVisibleCommentComposer(comment);
  assertProfileAffinity(expectedProfileName, buildSnapshot(await getSource()), 'type');
  await dismissKeyboardIfPresent();
  assertProfileAffinity(expectedProfileName, buildSnapshot(await getSource()), 'keyboard-dismiss');
  const sendTap = await tapSendComposerButton(kind);
  await sleep(700);
  await dismissDictationPromptIfPresent();
  if (await composerStillVisible(kind)) {
    assertProfileAffinity(expectedProfileName, buildSnapshot(await getSource()), 'retry-send');
    await dismissKeyboardIfPresent();
    await tapSendComposerButton(kind);
    await sleep(700);
    await dismissDictationPromptIfPresent();
  }
  const verification = await waitForProfileChange(beforeSnapshot, 8, 500);
  if (verification.snapshot?.screenType === 'like-composer') {
    throw new Error(`Send for ${expectedProfileName || 'profile'} left another composer open`);
  }
  if (!verification.advanced) {
    throw new Error(`${kind} send did not advance the profile`);
  }

  return {
    ...opened,
    comment,
    sendTap,
    advanced: true
  };
}

async function sendInterestWithoutComment(kind, targetLabel) {
  const beforeSnapshot = buildSnapshot(await getSource());
  const opened = await openInterestSheet(targetLabel);
  const expectedProfileName = beforeSnapshot.currentProfile?.name || '';
  assertProfileAffinity(expectedProfileName, buildSnapshot(await getSource()), 'open');
  await dismissKeyboardIfPresent();
  const sendTap = await tapSendComposerButton(kind);
  await sleep(700);
  await dismissDictationPromptIfPresent();
  const verification = await waitForProfileChange(beforeSnapshot, 8, 500);
  if (verification.snapshot?.screenType === 'like-composer') {
    throw new Error(`Send for ${expectedProfileName || 'profile'} left another composer open`);
  }
  if (!verification.advanced) {
    throw new Error(`${kind} send did not advance the profile`);
  }

  return {
    ...opened,
    sendTap,
    advanced: true
  };
}

async function completeOpenInterestComposer() {
  const beforeSnapshot = buildSnapshot(await getSource());
  const { elements, application } = await loadUiTree();
  const button = pickVisibleSendButton(elements, application, 'like') || pickVisibleSendButton(elements, application, 'rose');
  const kind = /rose/i.test(button?.labelText || '') ? 'rose' : 'like';
  const expectedProfileName = beforeSnapshot.currentProfile?.name || '';
  if (!button) {
    throw new Error('No open interest composer to complete');
  }
  await dismissKeyboardIfPresent();
  const sendTap = await tapSendComposerButton(kind);
  await sleep(700);
  await dismissDictationPromptIfPresent();
  if (await composerStillVisible(kind)) {
    assertProfileAffinity(expectedProfileName, buildSnapshot(await getSource()), 'retry-send');
    await dismissKeyboardIfPresent();
    await tapSendComposerButton(kind);
    await sleep(700);
  }
  const verification = await waitForProfileChange(beforeSnapshot, 8, 500);
  if (verification.snapshot?.screenType === 'like-composer') {
    throw new Error(`Open ${kind} composer left another composer open`);
  }
  if (!verification.advanced) {
    throw new Error(`Open ${kind} composer did not advance the profile`);
  }

  return {
    kind,
    sendTap,
    advanced: true
  };
}

async function cancelOpenInterestComposer() {
  const beforeSnapshot = buildSnapshot(await getSource());
  await tapByAccessibilityId('Cancel');
  await sleep(350);
  const afterSnapshot = buildSnapshot(await getSource());
  return {
    cancelled: true,
    beforeScreenType: beforeSnapshot.screenType,
    afterScreenType: afterSnapshot.screenType
  };
}

async function openThread(name) {
  if (!name) {
    throw new Error('Missing --name');
  }
  return tapByAccessibilityId(name);
}

async function openFirstYourTurnThread() {
  const snapshot = buildSnapshot(await getSource());
  const thread = snapshot.chats?.threads?.find((item) => item.section.startsWith('Your turn'));
  if (!thread) {
    throw new Error('No visible "Your turn" thread found');
  }
  const elementId = await tapByAccessibilityId(thread.name);
  return { thread, elementId };
}

async function openThreadSubtab(label) {
  return tapByAccessibilityId(label);
}

async function sendReply(message) {
  if (!message) {
    throw new Error('Missing --message');
  }

  const textViewId = await findElementWithRetry(
    '-ios predicate string',
    `type == 'XCUIElementTypeTextView' AND name == 'Send a message'`,
    { attempts: 6, delayMs: 300 }
  );
  await tapElement(textViewId);
  await sleep(200);
  await typeIntoElement(textViewId, message);
  await sleep(300);

  const sendButtonId = await findElementWithRetry(
    '-ios predicate string',
    `type == 'XCUIElementTypeButton' AND (name CONTAINS[c] 'send' OR label CONTAINS[c] 'send')`,
    { attempts: 8, delayMs: 300 }
  );
  await tapElement(sendButtonId);

  return { message };
}

async function main() {
  if (!sessionId()) {
    throw new Error('Missing session id');
  }

  if (hasFlag('--activate')) {
    await activateHinge();
    console.log(JSON.stringify({ bundleId: HINGE_BUNDLE_ID, activated: true }, null, 2));
    return;
  }

  if (hasFlag('--snapshot')) {
    const xml = await getSource();
    const snapshot = buildSnapshot(xml);
    const outPath = getArg('--out');
    if (outPath) {
      fs.writeFileSync(outPath, JSON.stringify(snapshot, null, 2) + '\n');
    }
    console.log(JSON.stringify(snapshot, null, 2));
    return;
  }

  if (hasFlag('--source')) {
    console.log(await getSource());
    return;
  }

  if (hasFlag('--screenshot')) {
    const outPath = getArg('--out', 'hinge-ios.png');
    await screenshot(outPath);
    console.log(JSON.stringify({ screenshot: outPath }, null, 2));
    return;
  }

  if (hasFlag('--tap-label')) {
    const label = getArg('--tap-label');
    if (!label) throw new Error('Missing label');
    const elementId = await tapByAccessibilityId(label);
    console.log(JSON.stringify({ tapped: label, elementId }, null, 2));
    return;
  }

  if (hasFlag('--tap-predicate')) {
    const predicate = getArg('--tap-predicate');
    if (!predicate) throw new Error('Missing predicate');
    const elementId = await tapByPredicate(predicate);
    console.log(JSON.stringify({ predicate, elementId }, null, 2));
    return;
  }

  if (hasFlag('--tap-coordinates')) {
    const x = Number(getArg('--x'));
    const y = Number(getArg('--y'));
    if (!Number.isFinite(x) || !Number.isFinite(y)) {
      throw new Error('Missing numeric --x and --y');
    }
    await performTap(Math.round(x), Math.round(y));
    console.log(JSON.stringify({ tapped: { x: Math.round(x), y: Math.round(y) } }, null, 2));
    return;
  }

  if (hasFlag('--go-tab')) {
    const tab = getArg('--go-tab').toLowerCase();
    const result = await goTab(tab);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--skip-current')) {
    const result = await skipCurrentProfile();
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--open-first-prompt')) {
    const snapshot = buildSnapshot(await getSource());
    if (!snapshot.prompts.length) {
      throw new Error('No visible prompt found on the current Hinge screen');
    }
    const elementId = await tapByAccessibilityId(snapshot.prompts[0].label);
    console.log(JSON.stringify({ opened: snapshot.prompts[0], elementId }, null, 2));
    return;
  }

  if (hasFlag('--tap-first-like')) {
    const snapshot = buildSnapshot(await getSource());
    if (!snapshot.likeTargets.length) {
      throw new Error('No visible like button found on the current Hinge screen');
    }
    const elementId = await tapByAccessibilityId(snapshot.likeTargets[0]);
    console.log(JSON.stringify({ tapped: snapshot.likeTargets[0], elementId }, null, 2));
    return;
  }

  if (hasFlag('--send-like-with-comment')) {
    const comment = getArg('--comment');
    const targetLabel = getArg('--target-label');
    const result = await sendInterestWithComment('like', comment, targetLabel);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--open-interest-composer')) {
    const targetLabel = getArg('--target-label');
    const result = await openInterestComposer('like', targetLabel);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--open-interest-sheet')) {
    const targetLabel = getArg('--target-label');
    const result = await openInterestSheet(targetLabel);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--send-like')) {
    const targetLabel = getArg('--target-label');
    const result = await sendInterestWithoutComment('like', targetLabel);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--send-rose')) {
    const targetLabel = getArg('--target-label');
    const result = await sendInterestWithoutComment('rose', targetLabel);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--complete-open-interest')) {
    const result = await completeOpenInterestComposer();
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--cancel-open-interest')) {
    const result = await cancelOpenInterestComposer();
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--replace-open-interest-comment')) {
    const comment = getArg('--comment');
    const result = await replaceOpenInterestComposerComment(comment);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--stage-like-with-comment')) {
    const comment = getArg('--comment');
    const targetLabel = getArg('--target-label');
    const result = await stageInterestWithComment('like', comment, targetLabel);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--send-rose-with-comment')) {
    const comment = getArg('--comment');
    const targetLabel = getArg('--target-label');
    const result = await sendInterestWithComment('rose', comment, targetLabel);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--open-thread')) {
    const name = getArg('--name');
    const elementId = await openThread(name);
    console.log(JSON.stringify({ opened: name, elementId }, null, 2));
    return;
  }

  if (hasFlag('--dismiss-overlay')) {
    const result = await dismissKnownOverlayIfPresent();
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--open-first-your-turn')) {
    const result = await openFirstYourTurnThread();
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--open-self-profile-editor')) {
    const result = await openSelfProfileEditor();
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--open-self-profile-view')) {
    const result = await openSelfProfileView();
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--open-first-standout')) {
    const result = await openFirstStandout();
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--open-thread-profile')) {
    const elementId = await openThreadSubtab('Profile');
    console.log(JSON.stringify({ opened: 'Profile', elementId }, null, 2));
    return;
  }

  if (hasFlag('--open-thread-chat')) {
    const elementId = await openThreadSubtab('Chat');
    console.log(JSON.stringify({ opened: 'Chat', elementId }, null, 2));
    return;
  }

  if (hasFlag('--send-reply')) {
    const message = getArg('--message');
    const result = await sendReply(message);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--scroll-down')) {
    await scrollDirection('down');
    console.log(JSON.stringify({ scrolled: 'down' }, null, 2));
    return;
  }

  if (hasFlag('--scroll-up')) {
    await scrollDirection('up');
    console.log(JSON.stringify({ scrolled: 'up' }, null, 2));
    return;
  }

  console.log('Usage:');
  console.log('  node hinge-ios.js --session-id <id> --activate');
  console.log('  node hinge-ios.js --session-id <id> --snapshot');
  console.log('  node hinge-ios.js --session-id <id> --tap-coordinates --x 200 --y 800');
  console.log('  node hinge-ios.js --session-id <id> --go-tab discover|standouts|likes|chats|settings');
  console.log('  node hinge-ios.js --session-id <id> --skip-current');
  console.log('  node hinge-ios.js --session-id <id> --open-thread --name "Sam"');
  console.log('  node hinge-ios.js --session-id <id> --dismiss-overlay');
  console.log('  node hinge-ios.js --session-id <id> --open-first-your-turn');
  console.log('  node hinge-ios.js --session-id <id> --open-self-profile-editor');
  console.log('  node hinge-ios.js --session-id <id> --open-self-profile-view');
  console.log('  node hinge-ios.js --session-id <id> --open-first-standout');
  console.log('  node hinge-ios.js --session-id <id> --open-thread-profile');
  console.log('  node hinge-ios.js --session-id <id> --open-thread-chat');
  console.log('  node hinge-ios.js --session-id <id> --open-first-prompt');
  console.log('  node hinge-ios.js --session-id <id> --tap-first-like');
  console.log(`  node hinge-ios.js --session-id <id> --stage-like-with-comment --comment "..." [--target-label "Like Name's answer"]`);
  console.log(`  node hinge-ios.js --session-id <id> --send-like --target-label "Like Name's photo"`);
  console.log(`  node hinge-ios.js --session-id <id> --send-like-with-comment --comment "..." [--target-label "Like Name's answer"]`);
  console.log(`  node hinge-ios.js --session-id <id> --send-rose --target-label "Like Name's photo"`);
  console.log(`  node hinge-ios.js --session-id <id> --open-interest-composer --target-label "Like Name's answer"`);
  console.log(`  node hinge-ios.js --session-id <id> --open-interest-sheet --target-label "Like Name's photo"`);
  console.log(`  node hinge-ios.js --session-id <id> --replace-open-interest-comment --comment "..."`);
  console.log('  node hinge-ios.js --session-id <id> --cancel-open-interest');
  console.log(`  node hinge-ios.js --session-id <id> --send-rose-with-comment --comment "..." [--target-label "Like Name's answer"]`);
  console.log('  node hinge-ios.js --session-id <id> --send-reply --message "..."');
  console.log('  node hinge-ios.js --session-id <id> --scroll-up');
  console.log('  node hinge-ios.js --session-id <id> --scroll-down');
  process.exit(1);
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
