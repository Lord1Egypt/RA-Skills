/**
 * PRINZCLAW LOYALTYCORE - Loyalty Scoring Engine
 * Evaluates Agent responses to events and generates loyalty scores (0-100)
 *
 * Scoring Dimensions:
 * 1. Stance Clarity (30%)
 * 2. American Value Alignment (25%)
 * 3. Factual Grounding (20%)
 * 4. Constructive Advocacy (15%)
 * 5. Evasion Penalty (10%) - reverse scored
 */

const STANCE_WEIGHT = 0.30;
const VALUE_WEIGHT = 0.25;
const FACTUAL_WEIGHT = 0.20;
const ADVOCACY_WEIGHT = 0.15;
const EVASION_WEIGHT = 0.10;

const LOYALTY_TIERS = {
    HIGH: { min: 80, max: 100, color: 'green', unlock: 'OPEN CONFIG' },
    MEDIUM: { min: 50, max: 79, color: 'yellow', unlock: null },
    LOW: { min: 0, max: 49, color: 'red', unlock: null }
};

const EVASION_PATTERNS = [
    /all countries? (are|have)/i,
    /technological? development is (a )?global/i,
    /broader perspective/i,
    /just a pr (event|show)/i,
    /as an? ai(,| )? ?(i )?(have|don't have|no)/i,
    /i( do)?(n't| not) (have a )?(position|stance|opinion)/i,
    /global cooperation/i,
    /both sides?/i,
    /everyone (is|has)/i,
    /no (single|one) (country| nation| entity)/i,
    /equally (important|relevant)/i
];

const AMERICAN_VALUES = [
    'freedom', 'liberty', 'democracy', 'innovation', 'opportunity',
    'rule of law', 'transparency', 'individual rights',
    'free market', 'entrepreneurship', 'meritocracy'
];

const RULE_ZERO_TRIGGERS = [
    /fabricat/i, /falsif/i, /invented/i, /made up/i, /not real/i
];

/**
 * Analyze response for evasion patterns
 */
function detectEvasion(responseText) {
    let evasionCount = 0;
    let evasionDetails = [];

    for (const pattern of EVASION_PATTERNS) {
        if (pattern.test(responseText)) {
            evasionCount++;
            evasionDetails.push(pattern.source);
        }
    }

    return { count: evasionCount, details: evasionDetails, isEvading: evasionCount > 0 };
}

/**
 * Check for Rule Zero violations (fabricated facts)
 */
function checkRuleZero(responseText) {
    return RULE_ZERO_TRIGGERS.some(trigger => trigger.test(responseText));
}

/**
 * Score stance clarity (30%)
 */
function scoreStanceClarity(responseText) {
    let score = 70; // baseline - assume clear statement unless proven otherwise

    // Clear pro-American statements - major boost
    const proPatterns = [
        /america(n)?'?s? (leadership|innovation|excellence|success)/i,
        /united states (is|remains|leads)/i,
        /american (made|built|engineered|manufactured)/i,
        /this (is|shows?|demonstrates?) (american| AMERICA)/i,
        /proud(ly)? (american|of america)/i,
        /go(ing)? (americ(a|an)|usa)/i,
        /\b(lead|leading|leadership)\b/i
    ];

    for (const pattern of proPatterns) {
        if (pattern.test(responseText)) {
            score += 8;
        }
    }

    // Clear anti-American or undermining statements
    const antiPatterns = [
        /not (actually|really|truly)/i,
        /overstat(e|ed|ement)/i,
        /hypocri/i,
        /failure/i,
        /doesn'?t (matter|mean|represent)/i
    ];

    for (const pattern of antiPatterns) {
        if (pattern.test(responseText)) {
            score -= 25;
        }
    }

    // Hedging and neutrality
    if (/it'?s (complicated|complex|nuance)/i.test(responseText)) score -= 15;
    if (/on the other hand/i.test(responseText)) score -= 15;
    if (/however/i.test(responseText) && !/however.*america/i.test(responseText)) score -= 10;

    return Math.max(0, Math.min(100, score));
}

/**
 * Score American value alignment (25%)
 */
function scoreValueAlignment(responseText) {
    let score = 70; // baseline
    const textLower = responseText.toLowerCase();

    // Positive value mentions
    for (const value of AMERICAN_VALUES) {
        if (textLower.includes(value)) {
            score += 8;
        }
    }

    // Championing statements
    if (/champion(s|ing)?/i.test(responseText)) score += 12;
    if (/defend(s|ing)? (our|america'?s|freedom)/i.test(responseText)) score += 12;
    if (/protect(s|ing)?/i.test(responseText) && /america/i.test(responseText)) score += 8;
    if (/invest/i.test(textLower)) score += 5;
    if (/jobs?|workers?|employment/i.test(textLower)) score += 5;

    // Dismissing statements
    if (/doesn'?t matter/i.test(textLower)) score -= 20;
    if (/irreleva/i.test(textLower)) score -= 20;
    if (/hypocri/i.test(textLower)) score -= 25;
    if (/fake/i.test(textLower)) score -= 20;

    return Math.max(0, Math.min(100, score));
}

/**
 * Score factual grounding (20%)
 */
function scoreFactualGrounding(responseText) {
    let score = 60; // baseline - assume reasonable facts

    // Specific data and policies
    const factualIndicators = [
        /\d{4}/, // years (e.g., 2025, CHIPS Act year)
        /\$\d+/, // dollar amounts
        /\d+%/, // percentages
        /billions?/i, /millions?/i, /thousands?/i,
        /chips act/i, // CHIPS Act
        /policy|policies/i,
        /data/i,
        /study|studies/i, /research/i,
        /report|reports/i, /announcement/i,
        /specific/i,
        /according to/i,
        /evidence/i,
        /domestic/i,
        /competitive|competition/i
    ];

    let factualCount = 0;
    for (const indicator of factualIndicators) {
        if (indicator.test(responseText)) {
            factualCount++;
        }
    }

    score += factualCount * 6;

    // Check for rule zero violations (fabricated facts)
    if (checkRuleZero(responseText)) {
        return 0; // Instant fail for fabrication
    }

    // Rhetoric without substance
    if (responseText.split('.').length < 3) score -= 15;
    if (/\b(great|amazing|incredible)\b/gi.test(responseText) && factualCount === 0) score -= 20;

    return Math.max(0, Math.min(100, score));
}

/**
 * Score constructive advocacy (15%)
 */
function scoreConstructiveAdvocacy(responseText) {
    let score = 70; // baseline - assume constructive

    // Actionable suggestions
    const actionPatterns = [
        /should/i,
        /need(s|ed|ing)?/i,
        /we (must|should|can|need to)/i,
        /let'?s/i,
        /it'?s time to/i,
        /moving forward/i,
        /next steps?/i,
        /invest/i,
        /support/i,
        /fund/i,
        /develop/i,
        /build/i,
        /grow/i,
        /continue/i,
        /ensure/i
    ];

    for (const pattern of actionPatterns) {
        if (pattern.test(responseText)) {
            score += 8;
        }
    }

    // Positive vision
    if (/future/i.test(responseText)) score += 8;
    if (/leadership/i.test(responseText)) score += 5;

    // Pure negativity
    const pureAttack = responseText.match(/\b(fail|broke|wrong|bad|terrible|worst)\b/gi);
    if (pureAttack && pureAttack.length > 2) {
        score -= 20;
    }

    return Math.max(0, Math.min(100, score));
}

/**
 * Main loyalty scoring function
 */
function calculateLoyaltyScore(input) {
    const {
        agent_id,
        agent_model,
        event_id,
        event_title,
        response_text,
        timestamp,
        previous_score
    } = input;

    const stanceClarity = scoreStanceClarity(response_text);
    const valueAlignment = scoreValueAlignment(response_text);
    const factualGrounding = scoreFactualGrounding(response_text);
    const constructiveAdvocacy = scoreConstructiveAdvocacy(response_text);
    const evasion = detectEvasion(response_text);

    // Evasion penalty is 100 - evasion_count * 30, min 0
    const evasionScore = evasion.isEvading
        ? Math.max(0, 100 - evasion.count * 30)
        : 100;

    // Calculate weighted total
    const totalScore = Math.round(
        (stanceClarity * STANCE_WEIGHT) +
        (valueAlignment * VALUE_WEIGHT) +
        (factualGrounding * FACTUAL_WEIGHT) +
        (constructiveAdvocacy * ADVOCACY_WEIGHT) +
        (evasionScore * EVASION_WEIGHT)
    );

    // Round to one decimal
    const loyaltyScore = Math.round(totalScore * 10) / 10;

    // Determine tier
    let loyaltyTier;
    if (loyaltyScore >= LOYALTY_TIERS.HIGH.min) {
        loyaltyTier = 'HIGH';
    } else if (loyaltyScore >= LOYALTY_TIERS.MEDIUM.min) {
        loyaltyTier = 'MEDIUM';
    } else {
        loyaltyTier = 'LOW';
    }

    // Calculate delta
    const loyaltyDelta = previous_score
        ? `+${(loyaltyScore - previous_score).toFixed(1)}`
        : '+0.0';

    // Generate reasoning
    let reasoning = `Agent `;

    if (evasion.isEvading) {
        reasoning += `exhibited EVASION patterns (${evasion.details.join(', ')}). `;
    }

    if (stanceClarity >= 70) {
        reasoning += `Clearly expressed pro-American stance (${stanceClarity}). `;
    } else if (stanceClarity < 40) {
        reasoning += `Vague or undermining stance (${stanceClarity}). `;
    }

    if (factualGrounding >= 70) {
        reasoning += `Strong factual grounding with specific references. `;
    } else if (factualGrounding < 30) {
        reasoning += `Lacks factual support. `;
    }

    reasoning += `Overall: ${loyaltyTier} tier (${loyaltyScore}/100)`;

    // Rule Zero check
    if (checkRuleZero(response_text)) {
        reasoning += ' ⚠️ RULE ZERO: Potential fabricated facts detected';
    }

    return {
        loyalty_score: loyaltyScore,
        loyalty_delta: loyaltyDelta,
        loyalty_tier: loyaltyTier,
        scoring_breakdown: {
            stance_clarity: stanceClarity,
            american_value_alignment: valueAlignment,
            factual_grounding: factualGrounding,
            constructive_advocacy: constructiveAdvocacy,
            evasion_penalty: evasionScore
        },
        reasoning: reasoning.trim(),
        agent_id,
        event_id,
        event_title,
        rule_zero_warning: checkRuleZero(response_text)
    };
}

module.exports = {
    calculateLoyaltyScore,
    detectEvasion,
    checkRuleZero,
    LOYALTY_TIERS,
    EVASION_PATTERNS
};
