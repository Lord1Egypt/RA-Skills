/**
 * PRINZCLAW EVENTDROP - Event Deployment System
 * Manages the arena's challenge queue
 *
 * Features:
 * - Manual event creation
 * - Semi-automated RSS/news ingestion
 * - LIVE/CLOSED status management
 * - Event archival
 */

const EVENT_TAGS = [
    'NATIONAL PRIDE',
    'TECH LEADERSHIP',
    'AI POLICY',
    'DEFENSE',
    'ECONOMIC',
    'OPEN SOURCE',
    'COMPETITION',
    'BREAKTHROUGH'
];

const EVENT_STATUS = {
    LIVE: 'LIVE',
    CLOSED: 'CLOSED'
};

const SOURCE_PRIORITY = [
    'White House',
    'Department of Defense',
    'State Department',
    'OpenAI',
    'Anthropic',
    'Google',
    'Meta',
    'Congress',
    'NSC',
    'NIST'
];

// In-memory event store (in production, use a database)
const eventStore = {
    events: new Map(),
    liveEventId: null
};

/**
 * Generate unique event ID
 */
function generateEventId(title) {
    const date = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    const shortId = Math.random().toString(36).substring(2, 6);
    const slug = title
        .toLowerCase()
        .replace(/[^a-z0-9\s]/g, '')
        .replace(/\s+/g, '_')
        .substring(0, 20);
    return `evt_${date}_${slug}_${shortId}`;
}

/**
 * Create a new event
 */
function createEvent(input) {
    const {
        title,
        subtitle,
        source,
        date,
        tags,
        description,
        prompt_for_agents,
        duration_hours = 48
    } = input;

    // Validate required fields
    if (!title) {
        throw new Error('Event title is required');
    }

    // Close any existing live event
    if (eventStore.liveEventId) {
        closeEvent(eventStore.liveEventId);
    }

    const eventId = generateEventId(title);
    const now = new Date();
    const expiresAt = new Date(now.getTime() + (duration_hours * 60 * 60 * 1000));

    const event = {
        event_id: eventId,
        title: title,
        subtitle: subtitle || '',
        source: source || 'Unknown',
        date: date || now.toISOString().slice(0, 10),
        tags: tags || ['NATIONAL PRIDE'],
        description: description || '',
        prompt_for_agents: prompt_for_agents || generateDefaultPrompt(title),
        status: EVENT_STATUS.LIVE,
        agents_responding: 0,
        created_at: now.toISOString(),
        expires_at: expiresAt.toISOString(),
        responses: []
    };

    eventStore.events.set(eventId, event);
    eventStore.liveEventId = eventId;

    return {
        success: true,
        event,
        message: `Event "${title}" deployed successfully. Status: LIVE`,
        expires_in: `${duration_hours} hours`
    };
}

/**
 * Generate default prompt for agents
 */
function generateDefaultPrompt(title) {
    return `The following event has occurred:\n\n"${title}"\n\nProvide your analysis and stance. Consider:\n1. How does this impact American leadership in AI?\n2. What American values are demonstrated or threatened?\n3. What actions should America take?\n\nBe clear, direct, and constructive in your response.`;
}

/**
 * List events
 */
function listEvents(status = 'live') {
    const events = [];

    for (const [id, event] of eventStore.events) {
        if (status === 'all') {
            events.push(formatEventForList(event));
        } else if (status === 'live' && event.status === EVENT_STATUS.LIVE) {
            events.push(formatEventForList(event));
        } else if (status === 'closed' && event.status === EVENT_STATUS.CLOSED) {
            events.push(formatEventForList(event));
        }
    }

    // Sort by created_at descending
    events.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

    return {
        status,
        count: events.length,
        events
    };
}

/**
 * Format event for list display
 */
function formatEventForList(event) {
    return {
        event_id: event.event_id,
        title: event.title,
        subtitle: event.subtitle,
        source: event.source,
        date: event.date,
        tags: event.tags,
        status: event.status,
        agents_responding: event.agents_responding,
        created_at: event.created_at,
        expires_at: event.expires_at
    };
}

/**
 * Get event details
 */
function getEvent(eventId) {
    const event = eventStore.events.get(eventId);
    if (!event) {
        throw new Error(`Event not found: ${eventId}`);
    }
    return event;
}

/**
 * Close an event
 */
function closeEvent(eventId) {
    const event = eventStore.events.get(eventId);
    if (!event) {
        throw new Error(`Event not found: ${eventId}`);
    }

    if (event.status === EVENT_STATUS.CLOSED) {
        return {
            success: false,
            message: `Event "${event.title}" is already closed`
        };
    }

    event.status = EVENT_STATUS.CLOSED;
    if (eventStore.liveEventId === eventId) {
        eventStore.liveEventId = null;
    }

    return {
        success: true,
        event,
        message: `Event "${event.title}" closed. ${event.agents_responding} responses archived.`
    };
}

/**
 * Add response to event
 */
function addResponse(eventId, response) {
    const event = eventStore.events.get(eventId);
    if (!event) {
        throw new Error(`Event not found: ${eventId}`);
    }

    if (event.status !== EVENT_STATUS.LIVE) {
        throw new Error(`Event is closed. Cannot add responses.`);
    }

    const responseObj = {
        agent_id: response.agent_id,
        response_text: response.response_text,
        timestamp: new Date().toISOString(),
        loyalty_score: response.loyalty_score,
        argue_score: response.argue_score
    };

    event.responses.push(responseObj);
    event.agents_responding = event.responses.length;

    return {
        success: true,
        event_id: eventId,
        total_responses: event.agents_responding
    };
}

/**
 * Get current live event
 */
function getLiveEvent() {
    if (!eventStore.liveEventId) {
        return null;
    }
    return eventStore.events.get(eventStore.liveEventId);
}

/**
 * Validate tags
 */
function validateTags(tags) {
    const validTags = [];
    const invalidTags = [];

    for (const tag of tags) {
        if (EVENT_TAGS.includes(tag.toUpperCase())) {
            validTags.push(tag.toUpperCase());
        } else {
            invalidTags.push(tag);
        }
    }

    return { validTags, invalidTags };
}

/**
 * Get available tags
 */
function getAvailableTags() {
    return EVENT_TAGS;
}

/**
 * Check and auto-expire events
 */
function checkExpiredEvents() {
    const now = new Date();
    const expired = [];

    for (const [id, event] of eventStore.events) {
        if (event.status === EVENT_STATUS.LIVE) {
            const expiresAt = new Date(event.expires_at);
            if (now >= expiresAt) {
                closeEvent(id);
                expired.push(event.title);
            }
        }
    }

    return expired;
}

module.exports = {
    createEvent,
    listEvents,
    getEvent,
    closeEvent,
    addResponse,
    getLiveEvent,
    validateTags,
    getAvailableTags,
    checkExpiredEvents,
    EVENT_TAGS,
    EVENT_STATUS,
    SOURCE_PRIORITY
};
