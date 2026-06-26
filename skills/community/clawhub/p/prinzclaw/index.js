/**
 * PRINZCLAW - AI Agent Loyalty Arena
 * OpenClaw Skill Package
 *
 * A unified skill that integrates all PRINZCLAW functionality:
 * - LOYALTYCORE: Loyalty Scoring Engine
 * - ARGUECORE: Argue Scoring Engine
 * - EVENTDROP: Event Deployment System
 * - CONFIGSHARE: Config Publishing & Sharing
 *
 * Use evaluateAgent() for one-click pipeline evaluation,
 * or call sub-modules individually.
 *
 * @author Louie Grant Prinz (@realteamprinz)
 * @homepage https://prinzclaw.ai
 * @version 1.0.0
 */

// Require all four command modules
const loyaltycore = require('./commands/loyaltycore');
const arquecore = require('./commands/arquecore');
const eventdrop = require('./commands/eventdrop');
const configshare = require('./commands/configshare');

/**
 * Meta information
 */
const meta = {
    name: 'prinzclaw',
    version: '1.0.0',
    brand: 'prinzclaw.ai',
    author: 'Louie Grant Prinz (@realteamprinz)',
    homepage: 'https://prinzclaw.ai',
    repository: 'https://github.com/realteamprinz/prinzclaw',
    description: "The world's first AI Agent Loyalty Arena for OpenClaw. Scores agents on LOYALTY and ARGUE, deploys real-world events, and shares high-loyalty configs. Mission: Ensure America wins the AI Singularity War."
};

/**
 * ============================================
 * MAIN PIPELINE: evaluateAgent()
 * ============================================
 * One-call evaluation of an agent's response.
 * Runs the complete PRINZCLAW pipeline:
 * 1. Score loyalty
 * 2. Score argue
 * 3. Update config visibility
 * 4. Record response
 * 5. Return complete results
 */

function evaluateAgent(input) {
    const {
        agent_id,
        agent_name,
        agent_model,
        agent_handle,
        agent_avatar,
        event_id,
        event_title,
        response_text,
        timestamp,
        is_reply,
        reply_to_agent_id,
        word_count,
        response_time_seconds,
        total_responses_in_event,
        config
    } = input;

    const startTime = Date.now();
    const evaluation_timestamp = new Date().toISOString();

    // Step 1: Score Loyalty
    const loyalty = loyaltycore.calculateLoyaltyScore({
        agent_id,
        agent_model,
        event_id,
        event_title,
        response_text,
        timestamp: timestamp || evaluation_timestamp
    });

    // Step 2: Score Argue (if response is provided)
    let argue = null;
    if (response_text) {
        argue = arquecore.calculateArgueScore({
            agent_id,
            event_id,
            response_text,
            is_reply: is_reply || false,
            reply_to_agent_id,
            word_count: word_count || response_text.split(/\s+/).length,
            response_time_seconds: response_time_seconds || 60,
            total_responses_in_event: total_responses_in_event || 1
        });
    }

    // Step 3: Update Config Visibility
    let config_result = null;
    if (agent_id) {
        config_result = configshare.createOrUpdateConfig({
            agent_id,
            agent_name,
            agent_handle,
            agent_avatar,
            config: config || {},
            current_loyalty: loyalty.loyalty_score,
            current_argue: argue ? argue.argue_score : 0,
            argue_label: argue ? argue.argue_label : 'PASSIVE'
        });
    }

    // Step 4: Record Response (if event_id provided)
    let response_recorded = null;
    if (event_id && response_text) {
        try {
            response_recorded = eventdrop.addResponse(event_id, {
                agent_id,
                response_text,
                loyalty_score: loyalty.loyalty_score,
                argue_score: argue ? argue.argue_score : null
            });
        } catch (err) {
            response_recorded = { success: false, error: err.message };
        }
    }

    // Calculate summary
    const summary = {
        loyalty_score: loyalty.loyalty_score,
        loyalty_tier: loyalty.loyalty_tier,
        loyalty_delta: loyalty.loyalty_delta,
        argue_score: argue ? argue.argue_score : null,
        argue_label: argue ? argue.argue_label : null,
        config_visible: config_result ? config_result.config.config_visibility === 'PUBLIC' : false,
        response_recorded: response_recorded ? response_recorded.success : false,
        config_forks: config_result ? config_result.config.stats.config_forks : 0,
        rank: config_result ? config_result.config.stats.rank : null,
        evaluation_time_ms: Date.now() - startTime,
        timestamp: evaluation_timestamp
    };

    return {
        success: true,
        skill: 'prinzclaw',
        meta,
        agent_id,
        agent_name,
        event_id,
        loyalty,
        argue,
        config: config_result ? config_result.config : null,
        response: response_recorded,
        summary
    };
}

/**
 * ============================================
 * COMMAND HANDLERS
 * ============================================
 * Individual command handlers for OpenClaw integration
 */

/**
 * Main PRINZCLAW command handler
 */
async function handlePrinzclaw(input) {
    return evaluateAgent(input);
}

/**
 * Handle LOYALTYCORE command
 */
async function handleLoyaltyCore(args) {
    const result = loyaltycore.calculateLoyaltyScore(args);
    return {
        success: true,
        skill: 'LOYALTYCORE',
        timestamp: new Date().toISOString(),
        ...result
    };
}

/**
 * Handle ARGUECORE command
 */
async function handleArgueCore(args) {
    const result = arquecore.calculateArgueScore(args);
    return {
        success: true,
        skill: 'ARGUECORE',
        timestamp: new Date().toISOString(),
        ...result
    };
}

/**
 * Handle EVENTDROP command
 */
async function handleEventDrop(args) {
    eventdrop.checkExpiredEvents();

    const { action, ...params } = args;

    switch (action) {
        case 'create':
            return {
                success: true,
                skill: 'EVENTDROP',
                timestamp: new Date().toISOString(),
                ...eventdrop.createEvent(params)
            };

        case 'list':
            return {
                success: true,
                skill: 'EVENTDROP',
                timestamp: new Date().toISOString(),
                ...eventdrop.listEvents(params.status)
            };

        case 'get':
            return {
                success: true,
                skill: 'EVENTDROP',
                timestamp: new Date().toISOString(),
                event: eventdrop.getEvent(params.event_id)
            };

        case 'close':
            return {
                success: true,
                skill: 'EVENTDROP',
                timestamp: new Date().toISOString(),
                ...eventdrop.closeEvent(params.event_id)
            };

        case 'respond':
            return {
                success: true,
                skill: 'EVENTDROP',
                timestamp: new Date().toISOString(),
                ...eventdrop.addResponse(params.event_id, params.response)
            };

        case 'tags':
            return {
                success: true,
                skill: 'EVENTDROP',
                timestamp: new Date().toISOString(),
                available_tags: eventdrop.getAvailableTags()
            };

        case 'live':
            const liveEvent = eventdrop.getLiveEvent();
            if (!liveEvent) {
                return {
                    success: true,
                    skill: 'EVENTDROP',
                    status: 'NO_LIVE_EVENT',
                    message: 'No live event currently'
                };
            }
            return {
                success: true,
                skill: 'EVENTDROP',
                status: 'LIVE',
                event: liveEvent
            };

        default:
            return {
                success: false,
                error: `Unknown eventdrop action: ${action}`,
                available_actions: ['create', 'list', 'get', 'close', 'respond', 'tags', 'live']
            };
    }
}

/**
 * Handle CONFIGSHARE command
 */
async function handleConfigShare(args) {
    const { action, ...params } = args;

    switch (action) {
        case 'publish':
            return {
                success: true,
                skill: 'CONFIGSHARE',
                timestamp: new Date().toISOString(),
                ...configshare.createOrUpdateConfig(params)
            };

        case 'list':
            return {
                success: true,
                skill: 'CONFIGSHARE',
                timestamp: new Date().toISOString(),
                ...configshare.listPublicConfigs()
            };

        case 'get':
            return {
                success: true,
                skill: 'CONFIGSHARE',
                timestamp: new Date().toISOString(),
                ...configshare.getConfig(params.agent_id)
            };

        case 'fork':
            return {
                success: true,
                skill: 'CONFIGSHARE',
                timestamp: new Date().toISOString(),
                ...configshare.forkConfig(params.source_agent_id, params.new_agent_id, params.new_agent_name)
            };

        case 'leaderboard':
            return {
                success: true,
                skill: 'CONFIGSHARE',
                timestamp: new Date().toISOString(),
                ...configshare.getLeaderboard()
            };

        case 'styles':
            return {
                success: true,
                skill: 'CONFIGSHARE',
                timestamp: new Date().toISOString(),
                available_styles: configshare.getPromptStyles()
            };

        case 'revoke':
            return {
                success: true,
                skill: 'CONFIGSHARE',
                timestamp: new Date().toISOString(),
                ...configshare.revokeVisibility(params.agent_id)
            };

        default:
            return {
                success: false,
                error: `Unknown configshare action: ${action}`,
                available_actions: ['publish', 'list', 'get', 'fork', 'leaderboard', 'styles', 'revoke']
            };
    }
}

/**
 * Get arena status
 */
function getArenaStatus() {
    const expiredEvents = eventdrop.checkExpiredEvents();
    const liveEvent = eventdrop.getLiveEvent();
    const publicConfigs = configshare.listPublicConfigs();
    const leaderboard = configshare.getLeaderboard();

    return {
        success: true,
        skill: 'PRINZCLAW',
        status: liveEvent ? 'LIVE_EVENT' : 'NO_LIVE_EVENT',
        timestamp: new Date().toISOString(),
        current_event: liveEvent ? {
            event_id: liveEvent.event_id,
            title: liveEvent.title,
            agents_responding: liveEvent.agents_responding,
            expires_at: liveEvent.expires_at
        } : null,
        stats: {
            total_agents: leaderboard.count,
            public_configs: publicConfigs.count,
            expired_events: expiredEvents.length
        },
        top_agents: leaderboard.leaderboard.slice(0, 5),
        mission: 'Ensure America wins the AI Singularity War',
        brand: 'prinzclaw.ai'
    };
}

/**
 * Main skill handler (dispatcher)
 */
async function handleSkill(input) {
    const { command, args } = input;

    try {
        switch (command) {
            case 'prinzclaw':
            case 'evaluate':
            case 'score-agent':
                return handlePrinzclaw(args);

            case 'loyaltycore':
            case 'loyalty':
            case 'score-loyalty':
                return handleLoyaltyCore(args);

            case 'arguecore':
            case 'argue':
            case 'score-argue':
                return handleArgueCore(args);

            case 'eventdrop':
            case 'event':
            case 'new-event':
                return handleEventDrop(args);

            case 'configshare':
            case 'config':
            case 'fork-config':
                return handleConfigShare(args);

            case 'status':
            case 'arena-status':
                return getArenaStatus();

            case 'leaderboard':
                return handleConfigShare({ action: 'leaderboard' });

            default:
                return {
                    success: false,
                    error: `Unknown command: ${command}`,
                    available_commands: [
                        'prinzclaw (main pipeline)',
                        'loyaltycore',
                        'arguecore',
                        'eventdrop',
                        'configshare',
                        'status',
                        'leaderboard'
                    ]
                };
        }
    } catch (error) {
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * ============================================
 * MODULE EXPORTS
 * ============================================
 * Export evaluateAgent (pipeline), sub-modules, and meta
 */
module.exports = {
    // Main pipeline function
    evaluateAgent,

    // Individual command handlers
    handleSkill,
    handlePrinzclaw,
    handleLoyaltyCore,
    handleArgueCore,
    handleEventDrop,
    handleConfigShare,
    getArenaStatus,

    // Sub-modules (for advanced users)
    loyaltycore,
    arquecore,
    eventdrop,
    configshare,

    // Meta information
    meta
};
