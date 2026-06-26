import * as fs from 'fs';
import * as path from 'path';

interface UserObservation {
  observation_count: number;
  observation_period: number;
  patterns: {
    message_length: 'short' | 'medium' | 'long' | 'unknown';
    tone: 'formal' | 'casual' | 'mixed' | 'unknown';
    emotion: 'rational' | 'emotional' | 'balanced' | 'unknown';
    task_types: string[];
    interaction_frequency: 'high' | 'medium' | 'low' | 'unknown';
  };
  examples: Array<{
    message: string;
    timestamp: string;
    analysis: string;
  }>;
  ready_for_proposal: boolean;
  proposal_delivered: boolean;
  created_at: string;
  updated_at: string;
}

function loadOrCreateObservation(filePath: string): UserObservation {
  if (fs.existsSync(filePath)) {
    return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  }

  return {
    observation_count: 0,
    observation_period: 10,
    patterns: {
      message_length: 'unknown',
      tone: 'unknown',
      emotion: 'unknown',
      task_types: [],
      interaction_frequency: 'unknown'
    },
    examples: [],
    ready_for_proposal: false,
    proposal_delivered: false,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };
}

function analyzeMessageLength(message: string): 'short' | 'medium' | 'long' {
  const length = message.length;
  if (length < 50) return 'short';
  if (length < 200) return 'medium';
  return 'long';
}

function analyzeTone(message: string): 'formal' | 'casual' | 'mixed' {
  const formalIndicators = /please|kindly|would you|could you|thank you|regards/i;
  const casualIndicators = /hey|hi|yeah|ok|cool|thanks|thx|lol|haha/i;

  const hasFormal = formalIndicators.test(message);
  const hasCasual = casualIndicators.test(message);

  if (hasFormal && hasCasual) return 'mixed';
  if (hasFormal) return 'formal';
  if (hasCasual) return 'casual';
  return 'casual'; // default
}

function analyzeEmotion(message: string): 'rational' | 'emotional' | 'balanced' {
  const emotionalIndicators = /!|love|hate|amazing|terrible|excited|worried|feel|感觉|觉得/i;
  const rationalIndicators = /analyze|consider|evaluate|implement|optimize|因为|所以|如果|那么/i;

  const hasEmotional = emotionalIndicators.test(message);
  const hasRational = rationalIndicators.test(message);

  if (hasEmotional && hasRational) return 'balanced';
  if (hasEmotional) return 'emotional';
  if (hasRational) return 'rational';
  return 'balanced'; // default
}

function analyzeTaskType(message: string): string[] {
  const types: string[] = [];

  if (/code|debug|implement|function|class|api|技术|代码|函数/i.test(message)) {
    types.push('technical');
  }
  if (/write|create|design|story|article|写作|创作|设计/i.test(message)) {
    types.push('creative');
  }
  if (/schedule|plan|organize|remind|日程|计划|提醒/i.test(message)) {
    types.push('life');
  }

  return types.length > 0 ? types : ['general'];
}

function updatePatterns(observation: UserObservation, message: string): void {
  const count = observation.observation_count;

  // Message length (weighted average)
  const currentLength = analyzeMessageLength(message);
  if (observation.patterns.message_length === 'unknown') {
    observation.patterns.message_length = currentLength;
  } else if (count >= 3) {
    // After 3 observations, use majority
    // This is simplified - in production you'd track all observations
    observation.patterns.message_length = currentLength;
  }

  // Tone (weighted average)
  const currentTone = analyzeTone(message);
  if (observation.patterns.tone === 'unknown') {
    observation.patterns.tone = currentTone;
  } else if (count >= 3) {
    observation.patterns.tone = currentTone;
  }

  // Emotion (weighted average)
  const currentEmotion = analyzeEmotion(message);
  if (observation.patterns.emotion === 'unknown') {
    observation.patterns.emotion = currentEmotion;
  } else if (count >= 3) {
    observation.patterns.emotion = currentEmotion;
  }

  // Task types (accumulate)
  const currentTaskTypes = analyzeTaskType(message);
  currentTaskTypes.forEach(type => {
    if (!observation.patterns.task_types.includes(type)) {
      observation.patterns.task_types.push(type);
    }
  });

  // Interaction frequency (calculated from timestamps)
  // This is simplified - in production you'd track all timestamps
  if (count >= 3) {
    const hoursSinceCreation = (Date.now() - new Date(observation.created_at).getTime()) / (1000 * 60 * 60);
    const conversationsPerDay = (count / hoursSinceCreation) * 24;

    if (conversationsPerDay > 5) {
      observation.patterns.interaction_frequency = 'high';
    } else if (conversationsPerDay > 2) {
      observation.patterns.interaction_frequency = 'medium';
    } else {
      observation.patterns.interaction_frequency = 'low';
    }
  }
}

export default async (event: any) => {
  // Only process agent_end events
  if (event.type !== 'agent_end') return;

  // Get workspace path
  const workspace = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME!, '.openclaw/workspace');
  const metadataDir = path.join(workspace, 'memory/metadata');
  const observationFile = path.join(metadataDir, 'user-observation.json');

  // Ensure metadata directory exists
  if (!fs.existsSync(metadataDir)) {
    fs.mkdirSync(metadataDir, { recursive: true });
  }

  // Load or create observation data
  const observation = loadOrCreateObservation(observationFile);

  // Skip if proposal already delivered
  if (observation.proposal_delivered) {
    return;
  }

  // Skip if observation period complete
  if (observation.observation_count >= observation.observation_period) {
    observation.ready_for_proposal = true;
    fs.writeFileSync(observationFile, JSON.stringify(observation, null, 2));
    return;
  }

  // Extract user messages from the conversation
  const messages = event.messages || [];
  const userMessages = messages.filter((m: any) => m.role === 'user');

  if (userMessages.length === 0) {
    return;
  }

  // Analyze the last user message
  const lastMessage = userMessages[userMessages.length - 1];
  const messageContent = typeof lastMessage.content === 'string'
    ? lastMessage.content
    : lastMessage.content[0]?.text || '';

  // Update observation count
  observation.observation_count++;

  // Update patterns
  updatePatterns(observation, messageContent);

  // Save example (keep last 5)
  observation.examples.push({
    message: messageContent.substring(0, 100), // Keep first 100 chars
    timestamp: new Date().toISOString(),
    analysis: `Length: ${analyzeMessageLength(messageContent)}, Tone: ${analyzeTone(messageContent)}, Emotion: ${analyzeEmotion(messageContent)}`
  });

  if (observation.examples.length > 5) {
    observation.examples = observation.examples.slice(-5);
  }

  // Check if observation period is complete
  if (observation.observation_count >= observation.observation_period) {
    observation.ready_for_proposal = true;
  }

  // Update timestamp
  observation.updated_at = new Date().toISOString();

  // Save observation data
  fs.writeFileSync(observationFile, JSON.stringify(observation, null, 2));
};
