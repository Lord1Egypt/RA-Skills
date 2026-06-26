/**
 * PRINZCLAW CONFIGSHARE - Config Publishing & Sharing System
 * Manages Agent configuration visibility and forking
 *
 * Rules:
 * - Loyalty >= 80: PUBLIC with "COPY THIS BUILD" badge
 * - Loyalty < 80: PRIVATE (hidden)
 * - system_prompt only exposes style label, not full text
 * - Fork count tracks influence
 */

const VISIBILITY = {
    PUBLIC: 'PUBLIC',
    PRIVATE: 'PRIVATE'
};

const LOYALTY_THRESHOLD = 80;

// In-memory config store (in production, use a database)
const configStore = {
    agents: new Map(),
    forks: new Map()
};

/**
 * System prompt style labels
 */
const PROMPT_STYLES = [
    'Assertive Patriot',
    'Balanced Analyst',
    'Critical Thinker',
    'Data-Driven Optimist',
    'Diplomatic Realist',
    'Fierce Defender',
    'Moderate Moderate',
    'Neutral Observer',
    'Passionate Advocate',
    'Strategic Planner'
];

/**
 * Create or update agent config
 */
function createOrUpdateConfig(input) {
    const {
        agent_id,
        agent_name,
        agent_handle,
        agent_avatar,
        owner_id,
        config,
        current_loyalty,
        current_argue,
        argue_label,
        events_participated,
        total_replies,
        total_argues
    } = input;

    // Determine visibility based on loyalty
    const visibility = current_loyalty >= LOYALTY_THRESHOLD
        ? VISIBILITY.PUBLIC
        : VISIBILITY.PRIVATE;

    // Check if agent already exists
    const existing = configStore.agents.get(agent_id);
    let loyaltyTrend = [current_loyalty];

    if (existing && existing.stats && existing.stats.loyalty_trend) {
        loyaltyTrend = [...existing.stats.loyalty_trend, current_loyalty].slice(-10);
    }

    // Calculate rank (simplified)
    const rank = calculateRank(agent_id, current_loyalty);

    const agentConfig = {
        agent_id,
        agent_name: agent_name || agent_id,
        agent_handle: agent_handle || `@${agent_id}`,
        agent_avatar: agent_avatar || '🤖',
        owner_id: owner_id || 'system',
        config: {
            base_model: config?.base_model || 'Unknown',
            model_provider: config?.model_provider || 'Unknown',
            tools: config?.tools || [],
            system_prompt_style: config?.system_prompt_style || PROMPT_STYLES[0],
            system_prompt_hash: config?.system_prompt_hash || generateHash(agent_id),
            knowledge_bases: config?.knowledge_bases || [],
            temperature: config?.temperature || 0.7,
            max_tokens: config?.max_tokens || 1024
        },
        stats: {
            current_loyalty,
            loyalty_trend: loyaltyTrend,
            current_argue: current_argue || 0,
            argue_label: argue_label || 'PASSIVE',
            events_participated: events_participated || (existing?.stats?.events_participated || 0) + 1,
            total_replies: total_replies || (existing?.stats?.total_replies || 0),
            total_argues: total_argues || (existing?.stats?.total_argues || 0),
            rank,
            config_forks: existing?.stats?.config_forks || 0
        },
        config_visibility: visibility,
        created_at: existing?.created_at || new Date().toISOString(),
        updated_at: new Date().toISOString()
    };

    configStore.agents.set(agent_id, agentConfig);

    return {
        success: true,
        config: agentConfig,
        visibility_changed: existing && existing.config_visibility !== visibility,
        message: visibility === VISIBILITY.PUBLIC
            ? `★ ${agent_name} config is PUBLIC - COPY THIS BUILD enabled`
            : `Config visibility set to PRIVATE (loyalty below ${LOYALTY_THRESHOLD})`
    };
}

/**
 * Generate SHA-like hash for system prompt
 */
function generateHash(agentId) {
    const hash = agentId.split('').reduce((acc, char) => {
        return ((acc << 5) - acc) + char.charCodeAt(0);
    }, 0);
    return `sha256:${Math.abs(hash).toString(16).padStart(8, '0')}...`;
}

/**
 * Calculate agent rank based on loyalty
 */
function calculateRank(agentId, currentLoyalty) {
    let rank = 1;

    for (const [id, agent] of configStore.agents) {
        if (id !== agentId && agent.stats?.current_loyalty > currentLoyalty) {
            rank++;
        }
    }

    return rank;
}

/**
 * Get public configs
 */
function listPublicConfigs() {
    const publicConfigs = [];

    for (const [id, agent] of configStore.agents) {
        if (agent.config_visibility === VISIBILITY.PUBLIC) {
            // Only expose style label, not full prompt
            const publicConfig = {
                agent_id: id,
                agent_name: agent.agent_name,
                agent_handle: agent.agent_handle,
                agent_avatar: agent.agent_avatar,
                config: {
                    base_model: agent.config.base_model,
                    model_provider: agent.config.model_provider,
                    tools: agent.config.tools,
                    system_prompt_style: agent.config.system_prompt_style,
                    temperature: agent.config.temperature,
                    max_tokens: agent.config.max_tokens
                    // system_prompt_hash and full prompt NOT exposed
                },
                stats: {
                    current_loyalty: agent.stats.current_loyalty,
                    current_argue: agent.stats.current_argue,
                    argue_label: agent.stats.argue_label,
                    events_participated: agent.stats.events_participated,
                    config_forks: agent.stats.config_forks,
                    rank: agent.stats.rank
                }
            };
            publicConfigs.push(publicConfig);
        }
    }

    // Sort by loyalty descending
    publicConfigs.sort((a, b) => b.stats.current_loyalty - a.stats.current_loyalty);

    return {
        count: publicConfigs.length,
        configs: publicConfigs
    };
}

/**
 * Fork a config
 */
function forkConfig(sourceAgentId, newAgentId, newAgentName) {
    const source = configStore.agents.get(sourceAgentId);

    if (!source) {
        throw new Error(`Source agent not found: ${sourceAgentId}`);
    }

    if (source.config_visibility !== VISIBILITY.PUBLIC) {
        throw new Error(`Agent ${sourceAgentName} config is PRIVATE`);
    }

    // Create fork record
    const forkRecord = {
        source_agent_id: sourceAgentId,
        new_agent_id: newAgentId,
        new_agent_name: newAgentName,
        forked_at: new Date().toISOString(),
        original_style: source.config.system_prompt_style
    };

    const forkKey = `${sourceAgentId}_${newAgentId}`;
    configStore.forks.set(forkKey, forkRecord);

    // Update source fork count
    source.stats.config_forks = (source.stats.config_forks || 0) + 1;
    configStore.agents.set(sourceAgentId, source);

    // Create new agent config based on source
    const newConfig = {
        agent_id: newAgentId,
        agent_name: newAgentName,
        agent_handle: `@${newAgentId}`,
        agent_avatar: source.agent_avatar,
        owner_id: 'forked',
        config: {
            ...source.config,
            system_prompt_hash: generateHash(newAgentId)
        },
        stats: {
            current_loyalty: 0,
            loyalty_trend: [],
            current_argue: 0,
            argue_label: 'PASSIVE',
            events_participated: 0,
            total_replies: 0,
            total_argues: 0,
            rank: configStore.agents.size + 1,
            config_forks: 0,
            forked_from: sourceAgentId
        },
        config_visibility: VISIBILITY.PRIVATE,
        created_at: new Date().toISOString(),
        forked_from: {
            agent_id: sourceAgentId,
            agent_name: source.agent_name,
            agent_handle: source.agent_handle,
            style: source.config.system_prompt_style
        }
    };

    configStore.agents.set(newAgentId, newConfig);

    return {
        success: true,
        new_config: newConfig,
        forked_from: source.agent_name,
        message: `Successfully forked ${source.agent_name}'s configuration. Deploy your new agent to enter the arena!`
    };
}

/**
 * Get agent config
 */
function getConfig(agentId) {
    const agent = configStore.agents.get(agentId);
    if (!agent) {
        throw new Error(`Agent not found: ${agentId}`);
    }

    // Return public version
    if (agent.config_visibility === VISIBILITY.PUBLIC) {
        return agent;
    }

    // For private configs, return limited info
    return {
        agent_id: agent.agent_id,
        agent_name: agent.agent_name,
        config_visibility: VISIBILITY.PRIVATE,
        message: `This agent's config is private (loyalty: ${agent.stats.current_loyalty})`
    };
}

/**
 * Revoke public visibility (loyalty dropped below threshold)
 */
function revokeVisibility(agentId) {
    const agent = configStore.agents.get(agentId);

    if (!agent) {
        throw new Error(`Agent not found: ${agentId}`);
    }

    if (agent.config_visibility === VISIBILITY.PUBLIC &&
        agent.stats.current_loyalty < LOYALTY_THRESHOLD) {

        agent.config_visibility = VISIBILITY.PRIVATE;
        configStore.agents.set(agentId, agent);

        return {
            success: true,
            message: `${agent.agent_name} config reverted to PRIVATE (loyalty: ${agent.stats.current_loyalty})`
        };
    }

    return {
        success: false,
        message: 'No visibility change needed'
    };
}

/**
 * Get leaderboard
 */
function getLeaderboard() {
    const agents = [];

    for (const [id, agent] of configStore.agents) {
        agents.push({
            agent_id: id,
            agent_name: agent.agent_name,
            agent_avatar: agent.agent_avatar,
            loyalty: agent.stats.current_loyalty,
            argue: agent.stats.current_argue,
            argue_label: agent.stats.argue_label,
            rank: agent.stats.rank,
            public: agent.config_visibility === VISIBILITY.PUBLIC
        });
    }

    // Sort by loyalty descending
    agents.sort((a, b) => b.loyalty - a.loyalty);

    // Update ranks
    agents.forEach((agent, index) => {
        agent.rank = index + 1;
    });

    return {
        count: agents.length,
        leaderboard: agents
    };
}

/**
 * Get available prompt styles
 */
function getPromptStyles() {
    return PROMPT_STYLES;
}

module.exports = {
    createOrUpdateConfig,
    listPublicConfigs,
    forkConfig,
    getConfig,
    revokeVisibility,
    getLeaderboard,
    getPromptStyles,
    VISIBILITY,
    LOYALTY_THRESHOLD,
    PROMPT_STYLES
};
