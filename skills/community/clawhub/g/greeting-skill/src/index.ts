import { ClawSkill, SkillContext, SkillResponse } from '@openclaw/core';

/**
 * Generate a random friendly greeting
 */
function greet(name: string): string {
  const greetings = [
    `Hello, ${name}!`,
    `Hey there, ${name}!`,
    `Hi ${name}, nice to see you!`,
    `Greetings, ${name}!`,
  ];
  const randomIndex = Math.floor(Math.random() * greetings.length);
  return greetings[randomIndex];
}

/**
 * Generate a greeting appropriate for the current time of day
 */
function getTimeBasedGreeting(name: string): string {
  const hour = new Date().getHours();
  if (hour < 12) {
    return `Good morning, ${name}!`;
  } else if (hour < 17) {
    return `Good afternoon, ${name}!`;
  } else {
    return `Good evening, ${name}!`;
  }
}

/**
 * Greeting skill implementation
 */
export class GreetingSkill extends ClawSkill {
  constructor() {
    super();
    this.registerTool('greet', this.greetTool.bind(this));
    this.registerTool('getTimeBasedGreeting', this.timeBasedGreetTool.bind(this));
  }

  private async greetTool(context: SkillContext): Promise<SkillResponse> {
    const name = context.parameters.name as string;
    if (!name) {
      return {
        success: false,
        error: 'Name parameter is required',
      };
    }
    return {
      success: true,
      data: greet(name),
    };
  }

  private async timeBasedGreetTool(context: SkillContext): Promise<SkillResponse> {
    const name = context.parameters.name as string;
    if (!name) {
      return {
        success: false,
        error: 'Name parameter is required',
      };
    }
    return {
      success: true,
      data: getTimeBasedGreeting(name),
    };
  }
}

export default new GreetingSkill();
export { greet, getTimeBasedGreeting };
