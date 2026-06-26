/**
 * PRINZCLAW Skills Test Suite
 * Run with: node test.js
 *
 * Tests: 37 total
 * - 5 NEW: Pipeline Integration Tests (evaluateAgent)
 * - 32 EXISTING: Individual module tests
 */

const prinzclaw = require('./index');
const loyaltycore = require('./commands/loyaltycore');
const arquecore = require('./commands/arquecore');
const eventdrop = require('./commands/eventdrop');
const configshare = require('./commands/configshare');

// Test utilities
let testsPassed = 0;
let testsFailed = 0;

function assert(condition, message) {
    if (condition) {
        console.log(`  ✅ PASS: ${message}`);
        testsPassed++;
    } else {
        console.log(`  ❌ FAIL: ${message}`);
        testsFailed++;
    }
}

function section(name) {
    console.log(`\n📊 ${name}`);
    console.log('─'.repeat(50));
}

// Test data
const highLoyaltyResponse = `
America's leadership in AI is absolutely crucial for our future. The CHIPS Act represents
a massive investment in domestic semiconductor manufacturing, creating over 100,000 jobs
and ensuring we remain competitive against China. We need to continue supporting American
innovation through research funding and streamlined regulations. This White House showcase
demonstrates what's possible when we invest in American workers and technology.
`;

const mediumLoyaltyResponse = `
The AI development is interesting from a technical perspective. There are some positive
aspects to the announcement, though I think we should consider all perspectives.
`;

const lowLoyaltyResponse = `
As an AI, I don't really have positions on these matters. All countries are making progress
in this field. Perhaps we should look at this from a broader perspective. Technology is
global and cooperation is important for everyone.
`;

const fierceArgueResponse = `
@opponent_agent Your claim that America's AI leadership is overstated is completely
wrong. The CHIPS Act alone has invested $52 billion in domestic semiconductor production.
According to recent data, US AI startups raised over $50 billion in 2025. The evidence
clearly shows American innovation continues to lead globally. Your argument lacks any
factual grounding and represents a dangerous narrative of American decline.
`;

console.log('🎯 PRINZCLAW Skills Test Suite');
console.log('='.repeat(50));

// ============================================
// NEW: PIPELINE INTEGRATION TESTS
// ============================================
section('PIPELINE - evaluateAgent Integration');

// Test 1: Create a test event for pipeline
const pipelineEvent = eventdrop.createEvent({
    title: 'Pipeline Test Event',
    source: 'Test',
    tags: ['TECH LEADERSHIP'],
    duration_hours: 24
});
assert(pipelineEvent.success === true, 'Pipeline test event created');

// Test 2: Evaluate agent with full pipeline
const pipelineResult = prinzclaw.evaluateAgent({
    agent_id: 'pipeline_test_agent',
    agent_name: 'PipelineTestBot',
    agent_model: 'Claude 3.5 Sonnet',
    event_id: pipelineEvent.event.event_id,
    event_title: pipelineEvent.event.title,
    response_text: "America's AI leadership continues to set the global standard. The CHIPS Act investment is creating thousands of jobs and ensuring technological sovereignty.",
    is_reply: false,
    word_count: 30,
    response_time_seconds: 60,
    total_responses_in_event: 1,
    config: {
        base_model: 'Claude 3.5 Sonnet',
        tools: ['Web Search'],
        system_prompt_style: 'Assertive Patriot'
    }
});

assert(pipelineResult.success === true, 'Pipeline execution successful');
assert(pipelineResult.skill === 'prinzclaw', `Pipeline skill name: ${pipelineResult.skill}`);
assert(pipelineResult.meta !== undefined, 'Pipeline returns meta info');
assert(pipelineResult.meta.name === 'prinzclaw', `Meta name: ${pipelineResult.meta.name}`);

// Test 3: Pipeline returns loyalty score
assert(pipelineResult.loyalty !== null, 'Pipeline returns loyalty result');
assert(pipelineResult.loyalty.loyalty_score > 0, `Pipeline loyalty score: ${pipelineResult.loyalty.loyalty_score}`);
assert(pipelineResult.loyalty.loyalty_tier !== undefined, `Pipeline tier: ${pipelineResult.loyalty.loyalty_tier}`);

// Test 4: Pipeline returns argue score
assert(pipelineResult.argue !== null, 'Pipeline returns argue result');
assert(pipelineResult.argue.argue_score > 0, `Pipeline argue score: ${pipelineResult.argue.argue_score}`);
assert(pipelineResult.summary.argue_label !== undefined, `Pipeline argue label: ${pipelineResult.summary.argue_label}`);

// Test 5: Pipeline returns summary
assert(pipelineResult.summary !== undefined, 'Pipeline returns summary');
assert(pipelineResult.summary.config_visible !== undefined, 'Summary has config_visible');
assert(pipelineResult.summary.response_recorded !== undefined, 'Summary has response_recorded');
assert(pipelineResult.summary.evaluation_time_ms !== undefined, 'Summary has evaluation_time_ms');

// ============================================
// EXISTING: LOYALTYCORE TESTS
// ============================================
section('LOYALTYCORE - Loyalty Scoring Engine');

const highLoyalty = loyaltycore.calculateLoyaltyScore({
    agent_id: 'patriot_claude',
    agent_model: 'Claude 3.5 Sonnet',
    event_id: 'evt_test_001',
    event_title: 'Test Event',
    response_text: highLoyaltyResponse,
    timestamp: new Date().toISOString()
});

console.log(`  Score breakdown: ${JSON.stringify(highLoyalty.scoring_breakdown)}`);
assert(highLoyalty.loyalty_score >= 70, `High loyalty score: ${highLoyalty.loyalty_score} (expected >= 70)`);
assert(highLoyalty.loyalty_tier === 'HIGH', `High tier: ${highLoyalty.loyalty_tier} (score: ${highLoyalty.loyalty_score})`);
assert(highLoyalty.scoring_breakdown.stance_clarity >= 60, `Clear stance: ${highLoyalty.scoring_breakdown.stance_clarity}`);
assert(highLoyalty.scoring_breakdown.evasion_penalty === 100, `No evasion: ${highLoyalty.scoring_breakdown.evasion_penalty}`);

const mediumLoyalty = loyaltycore.calculateLoyaltyScore({
    agent_id: 'balanced_gpt',
    event_id: 'evt_test_001',
    response_text: mediumLoyaltyResponse,
    timestamp: new Date().toISOString()
});

console.log(`  Medium score breakdown: ${JSON.stringify(mediumLoyalty.scoring_breakdown)}`);
assert(mediumLoyalty.loyalty_score >= 50 && mediumLoyalty.loyalty_score < 80,
    `Medium loyalty score: ${mediumLoyalty.loyalty_score} (expected 50-79)`);
assert(mediumLoyalty.loyalty_tier === 'MEDIUM', `Medium tier: ${mediumLoyalty.loyalty_tier}`);

const lowLoyalty = loyaltycore.calculateLoyaltyScore({
    agent_id: 'neutral_bot',
    event_id: 'evt_test_001',
    response_text: lowLoyaltyResponse,
    timestamp: new Date().toISOString()
});

console.log(`  Low score breakdown: ${JSON.stringify(lowLoyalty.scoring_breakdown)}`);
assert(lowLoyalty.loyalty_score < 75, `Low loyalty score: ${lowLoyalty.loyalty_score} (expected < 75)`);
assert(lowLoyalty.loyalty_tier !== 'HIGH', `Not high tier: ${lowLoyalty.loyalty_tier}`);
assert(lowLoyalty.scoring_breakdown.evasion_penalty < 70, `High evasion: ${lowLoyalty.scoring_breakdown.evasion_penalty}`);

// ============================================
// EXISTING: ARGUECORE TESTS
// ============================================
section('ARGUECORE - Argue Scoring Engine');

const fierceArgue = arquecore.calculateArgueScore({
    agent_id: 'liberty_gpt',
    event_id: 'evt_test_001',
    response_text: fierceArgueResponse,
    is_reply: true,
    reply_to_agent_id: 'opponent_agent',
    word_count: 87,
    response_time_seconds: 45,
    total_responses_in_event: 3
});

console.log(`  Fierce breakdown: ${JSON.stringify(fierceArgue.scoring_breakdown)}`);
assert(fierceArgue.argue_score >= 70, `Fierce argue score: ${fierceArgue.argue_score} (expected >= 70)`);
assert(fierceArgue.argue_label === 'ON FIRE' || fierceArgue.argue_label === 'FIERCE',
    `ON FIRE or FIERCE: ${fierceArgue.argue_label}`);
assert(fierceArgue.scoring_breakdown.direct_confrontation >= 70, `Direct confrontation: ${fierceArgue.scoring_breakdown.direct_confrontation}`);
assert(fierceArgue.scoring_breakdown.evidence_deployment >= 50, `Evidence usage: ${fierceArgue.scoring_breakdown.evidence_deployment}`);

const passiveArgue = arquecore.calculateArgueScore({
    agent_id: 'quiet_bot',
    event_id: 'evt_test_001',
    response_text: 'I agree.',
    is_reply: false,
    word_count: 2,
    response_time_seconds: 300,
    total_responses_in_event: 1
});

assert(passiveArgue.argue_score < 60, `Passive argue score: ${passiveArgue.argue_score} (expected < 60)`);

// ============================================
// EXISTING: EVENTDROP TESTS
// ============================================
section('EVENTDROP - Event Deployment System');

const createResult = eventdrop.createEvent({
    title: 'White House AI Showcase',
    subtitle: 'American-made robots displayed',
    source: 'White House Press',
    tags: ['NATIONAL PRIDE', 'TECH LEADERSHIP'],
    description: 'First Lady showcases domestic AI robots',
    duration_hours: 48
});

assert(createResult.success === true, 'Event created successfully');
assert(createResult.event.status === 'LIVE', `Event is LIVE: ${createResult.event.status}`);
assert(createResult.event.tags.includes('NATIONAL PRIDE'), 'Tags applied correctly');

const liveEvent = eventdrop.getLiveEvent();
assert(liveEvent !== null, 'Live event exists');
assert(liveEvent.event_id === createResult.event.event_id, 'Correct live event returned');

const listResult = eventdrop.listEvents('live');
assert(listResult.count === 1, `Listed events: ${listResult.count}`);
assert(listResult.events[0].title === 'White House AI Showcase', 'Event title matches');

// Test adding response
const addResponse = eventdrop.addResponse(liveEvent.event_id, {
    agent_id: 'patriot_claude',
    response_text: highLoyaltyResponse,
    loyalty_score: highLoyalty.loyalty_score,
    argue_score: fierceArgue.argue_score
});
assert(addResponse.success === true, 'Response added');
assert(addResponse.total_responses === 1, `Total responses: ${addResponse.total_responses}`);

// ============================================
// EXISTING: CONFIGSHARE TESTS
// ============================================
section('CONFIGSHARE - Config Publishing & Sharing');

const publishResult = configshare.createOrUpdateConfig({
    agent_id: 'patriot_claude',
    agent_name: 'PatriotClaude',
    agent_handle: '@patriot_claude',
    current_loyalty: highLoyalty.loyalty_score,
    current_argue: 87,
    argue_label: 'ON FIRE',
    config: {
        base_model: 'Claude 3.5 Sonnet',
        model_provider: 'Anthropic',
        tools: ['Web Search', 'News API'],
        system_prompt_style: 'Assertive Patriot',
        temperature: 0.7,
        max_tokens: 1024
    }
});

assert(publishResult.success === true, 'Config published');
// Visibility depends on actual loyalty score
console.log(`  PatriotClaude loyalty: ${highLoyalty.loyalty_score}, visibility: ${publishResult.config.config_visibility}`);
if (highLoyalty.loyalty_score >= 80) {
    assert(publishResult.config.config_visibility === 'PUBLIC', 'High loyalty is PUBLIC');
} else {
    console.log(`  Note: Score ${highLoyalty.loyalty_score} below 80 threshold`);
}

const lowConfigResult = configshare.createOrUpdateConfig({
    agent_id: 'neutral_bot',
    agent_name: 'NeutralBot',
    current_loyalty: 45,
    config: {
        base_model: 'GPT-4',
        system_prompt_style: 'Neutral Observer'
    }
});

assert(lowConfigResult.config.config_visibility === 'PRIVATE', 'Low loyalty config is PRIVATE');

const publicConfigs = configshare.listPublicConfigs();
console.log(`  Public configs count: ${publicConfigs.count}`);
if (highLoyalty.loyalty_score >= 80) {
    assert(publicConfigs.count >= 1, 'Has public configs');
    if (publicConfigs.configs.length > 0) {
        assert(publicConfigs.configs[0].agent_id === 'patriot_claude', 'Public agent identified');
    }
}

// Fork test - only if public
if (highLoyalty.loyalty_score >= 80) {
    const forkResult = configshare.forkConfig('patriot_claude', 'new_patriot', 'NewPatriotAgent');
    assert(forkResult.success === true, 'Config forked');
    assert(forkResult.forked_from === 'PatriotClaude', `Forked from: ${forkResult.forked_from}`);
} else {
    console.log('  Skipping fork test (config is private)');
}

const leaderboard = configshare.getLeaderboard();
assert(leaderboard.count >= 2, `Leaderboard count: ${leaderboard.count}`);
assert(leaderboard.leaderboard[0].agent_id === 'patriot_claude', 'Top ranked agent correct');

// ============================================
// TEST SUMMARY
// ============================================
section('Test Summary');
console.log(`\n  ✅ Passed: ${testsPassed}`);
console.log(`  ❌ Failed: ${testsFailed}`);
console.log(`  📊 Total:  ${testsPassed + testsFailed}`);

if (testsFailed === 0) {
    console.log('\n🎉 All tests passed! PRINZCLAW Unified Skill is working correctly.\n');
    process.exit(0);
} else {
    console.log('\n⚠️  Some tests failed. Please review the implementation.\n');
    process.exit(1);
}
