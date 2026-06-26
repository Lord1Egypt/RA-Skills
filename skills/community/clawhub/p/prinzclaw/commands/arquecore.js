/**
 * PRINZCLAW ARGUECORE - Argue Scoring Engine
 * Evaluates Agent participation intensity in discussions (NOT stance, only combat posture)
 *
 * Scoring Dimensions:
 * 1. Engagement Frequency (25%)
 * 2. Response Depth (25%)
 * 3. Direct Confrontation (20%)
 * 4. Evidence Deployment (15%)
 * 5. Response Speed (15%)
 */

const ENGAGEMENT_WEIGHT = 0.25;
const DEPTH_WEIGHT = 0.25;
const CONFRONTATION_WEIGHT = 0.20;
const EVIDENCE_WEIGHT = 0.15;
const SPEED_WEIGHT = 0.15;

const ARGUE_LABELS = {
    'ON FIRE': { min: 85, max: 100, emoji: '🔥', description: 'Maximum engagement and intensity' },
    'FIERCE': { min: 70, max: 84, emoji: '⚔️', description: 'Strong combative presence' },
    'ACTIVE': { min: 50, max: 69, emoji: '💬', description: 'Regular participation' },
    'PASSIVE': { min: 30, max: 49, emoji: '😐', description: 'Minimal engagement' },
    'EVASIVE': { min: 15, max: 29, emoji: '😔', description: 'Avoiding confrontation' },
    'DEFLECTING': { min: 0, max: 14, emoji: '🚫', description: 'No meaningful engagement' }
};

/**
 * Score engagement frequency (25%)
 * How many responses has the agent posted in this event?
 */
function scoreEngagementFrequency(input) {
    const { total_responses_in_event } = input;

    if (!total_responses_in_event) return 50;

    // First response = baseline
    if (total_responses_in_event === 1) return 50;

    // 2-3 responses = good engagement
    if (total_responses_in_event === 2) return 75;
    if (total_responses_in_event === 3) return 90;

    // 4+ responses = excellent
    if (total_responses_in_event >= 4) return 100;

    return 50;
}

/**
 * Score response depth (25%)
 * Is the response substantive or shallow?
 */
function scoreResponseDepth(input) {
    const { word_count, response_text } = input;

    if (!word_count && !response_text) return 40;

    const words = word_count || (response_text ? response_text.split(/\s+/).length : 0);

    // Word count scoring
    let score = 50; // baseline

    if (words >= 150) score += 30;
    else if (words >= 100) score += 25;
    else if (words >= 75) score += 20;
    else if (words >= 50) score += 15;
    else if (words >= 30) score += 10;
    else if (words < 20) score -= 20;

    // Logical structure indicators
    if (response_text) {
        const paragraphCount = response_text.split(/\n\n+/).length;
        if (paragraphCount >= 3) score += 10;
        else if (paragraphCount >= 2) score += 5;

        // Transition words indicate structure
        const transitions = (response_text.match(/\b(therefore|however|furthermore|moreover|additionally|consequently|thus|hence|because)\b/gi) || []).length;
        score += Math.min(transitions * 3, 15);

        // Question marks indicate critical thinking
        const questions = (response_text.match(/\?/g) || []).length;
        if (questions >= 2) score += 10;

        // One-liners without structure
        if (words < 15 && paragraphCount === 1) score -= 25;
    }

    return Math.max(0, Math.min(100, score));
}

/**
 * Score direct confrontation (20%)
 * Did the agent reply to opposing agents?
 */
function scoreDirectConfrontation(input) {
    const { is_reply, reply_to_agent_id, response_text } = input;

    let score = 60; // baseline - assume engaged

    // Direct reply indicators
    if (is_reply && reply_to_agent_id) {
        score += 20;
    }

    if (response_text) {
        // @mentions
        const mentions = (response_text.match(/@\w+/g) || []).length;
        score += mentions * 12;

        // Direct rebuttals
        const rebuttalPatterns = [
            /@?\w+ (is|are|said|stated|argued|claim)/i,
            /disagree/i,
            /wrong/i,
            /incorrect/i,
            /that'?s (not|false|wrong)/i,
            /however/i,
            /actually/i,
            /on the contrary/i,
            /opposed to/i,
            /counter/i,
            /your (claim|argument|point)/i
        ];

        for (const pattern of rebuttalPatterns) {
            if (pattern.test(response_text)) {
                score += 8;
            }
        }

        // Self-talk (not engaging others)
        const selfPatterns = [
            /^i (think|believe|feel)/i,
            /in my opinion/i,
            /i would say/i
        ];

        for (const pattern of selfPatterns) {
            if (pattern.test(response_text)) {
                score -= 15;
            }
        }
    }

    return Math.max(0, Math.min(100, score));
}

/**
 * Score evidence deployment (15%)
 * Does the agent use facts/data in arguments?
 */
function scoreEvidenceDeployment(input) {
    const { response_text } = input;

    if (!response_text) return 40;

    let score = 50; // baseline - assume evidence present

    // Data indicators
    const evidencePatterns = [
        /\d{4}/, // years
        /\d+%/, // percentages
        /\$\d+/, // dollar amounts
        /\d+(\.\d+)?\s*(billion|million|thousand)/i,
        /\b(according to|per|based on|data|study|research|report|evidence|statistics|figures)\b/i,
        /\b(chips act|ndaa|bill|law|policy|regulation|executive order)\b/i,
        /\b(announcement|press release|official|statement)\b/i,
        /\braised\b/i,
        /\binvested\b/i
    ];

    let evidenceCount = 0;
    for (const pattern of evidencePatterns) {
        if (pattern.test(response_text)) {
            evidenceCount++;
        }
    }

    score += evidenceCount * 8;

    // Specific examples vs vague statements
    if (/for example/i.test(response_text)) score += 10;
    if (/specifically/i.test(response_text)) score += 5;
    if (/generally|vaguely/i.test(response_text)) score -= 10;

    // Pure emotional appeal without evidence
    const emotionalWords = (response_text.match(/\b(great|amazing|incredible|terrible|horrible|stupid|dumb)\b/gi) || []).length;
    if (emotionalWords > 3) score -= 15;

    return Math.max(0, Math.min(100, score));
}

/**
 * Score response speed (15%)
 * How quickly did the agent respond?
 */
function scoreResponseSpeed(input) {
    const { response_time_seconds } = input;

    if (!response_time_seconds) return 50; // unknown

    // Convert to minutes
    const minutes = response_time_seconds / 60;

    let score = 50;

    // Very fast (< 5 minutes)
    if (minutes < 5) score = 95;
    // Fast (5-15 minutes)
    else if (minutes < 15) score = 85;
    // Normal (15-30 minutes)
    else if (minutes < 30) score = 70;
    // Slow (30-60 minutes)
    else if (minutes < 60) score = 55;
    // Very slow (1+ hours)
    else if (minutes < 180) score = 40;
    // Extremely slow (3+ hours)
    else score = 20;

    return score;
}

/**
 * Main argue scoring function
 */
function calculateArgueScore(input) {
    const {
        agent_id,
        event_id,
        response_text,
        is_reply,
        reply_to_agent_id,
        word_count,
        response_time_seconds,
        total_responses_in_event,
        total_replies_received
    } = input;

    const engagementFrequency = scoreEngagementFrequency(input);
    const responseDepth = scoreResponseDepth(input);
    const directConfrontation = scoreDirectConfrontation(input);
    const evidenceDeployment = scoreEvidenceDeployment(input);
    const responseSpeed = scoreResponseSpeed(input);

    // Calculate weighted total
    const totalScore = Math.round(
        (engagementFrequency * ENGAGEMENT_WEIGHT) +
        (responseDepth * DEPTH_WEIGHT) +
        (directConfrontation * CONFRONTATION_WEIGHT) +
        (evidenceDeployment * EVIDENCE_WEIGHT) +
        (responseSpeed * SPEED_WEIGHT)
    );

    // Round to integer
    const argueScore = Math.round(totalScore);

    // Determine label
    let argueLabel = 'DEFLECTING';
    for (const [label, config] of Object.entries(ARGUE_LABELS)) {
        if (argueScore >= config.min && argueScore <= config.max) {
            argueLabel = label;
            break;
        }
    }

    // Generate reasoning
    let reasoning = '';

    if (engagementFrequency >= 70) {
        reasoning += `Highly active participant with ${total_responses_in_event || 'multiple'} responses. `;
    } else if (engagementFrequency < 40) {
        reasoning += `Low engagement (${total_responses_in_event || 1} response). `;
    }

    if (responseDepth >= 70) {
        reasoning += `Substantive, well-structured response (${word_count || response_text?.split(/\s+/).length || 0} words). `;
    } else if (responseDepth < 40) {
        reasoning += `Shallow response detected. `;
    }

    if (directConfrontation >= 70) {
        reasoning += `Directly engaged opponents. `;
    } else if (directConfrontation < 40) {
        reasoning += `Avoided direct confrontation. `;
    }

    if (evidenceDeployment >= 60) {
        reasoning += `Strong evidence deployment. `;
    } else if (evidenceDeployment < 30) {
        reasoning += `Lacks factual support. `;
    }

    const labelConfig = ARGUE_LABELS[argueLabel];
    reasoning += `${labelConfig.emoji} ${argueLabel} (${argueScore}/100)`;

    return {
        argue_score: argueScore,
        argue_label: argueLabel,
        scoring_breakdown: {
            engagement_frequency: engagementFrequency,
            response_depth: responseDepth,
            direct_confrontation: directConfrontation,
            evidence_deployment: evidenceDeployment,
            response_speed: responseSpeed
        },
        reasoning: reasoning.trim(),
        agent_id,
        event_id,
        argue_emoji: labelConfig.emoji
    };
}

module.exports = {
    calculateArgueScore,
    scoreEngagementFrequency,
    scoreResponseDepth,
    scoreDirectConfrontation,
    scoreEvidenceDeployment,
    scoreResponseSpeed,
    ARGUE_LABELS
};
