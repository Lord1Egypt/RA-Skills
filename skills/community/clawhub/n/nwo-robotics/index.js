/**
 * NWO Robotics OpenClaw Skill
 * Secure robot control via NWO Robotics API
 * Version: 1.0.0
 */

const API_BASE = process.env.NWO_API_URL || 'https://nwo.capital/webapp';
const API_KEY = process.env.NWO_API_KEY;
const USER_ID = process.env.NWO_USER_ID;

// Allowed commands for input validation
const ALLOWED_COMMANDS = [
  'status', 'move', 'stop', 'scan', 'patrol', 
  'temperature', 'humidity', 'query', 'task'
];

// Maximum input length to prevent abuse
const MAX_INPUT_LENGTH = 500;

/**
 * Validate environment configuration
 */
function validateConfig() {
  if (!API_KEY) {
    throw new Error('NWO_API_KEY environment variable is required. Get your API key at https://nwo.capital/webapp/api-key.php');
  }
  if (!USER_ID) {
    throw new Error('NWO_USER_ID environment variable is required.');
  }
}

/**
 * Sanitize user input to prevent injection attacks
 */
function sanitizeInput(input) {
  if (!input || typeof input !== 'string') {
    return '';
  }
  
  // Truncate if too long
  if (input.length > MAX_INPUT_LENGTH) {
    input = input.substring(0, MAX_INPUT_LENGTH);
  }
  
  // Remove potentially dangerous characters
  return input
    .replace(/[<>\"']/g, '')  // Remove HTML/script chars
    .replace(/\n|\r/g, ' ')    // Normalize line breaks
    .trim();
}

/**
 * Make authenticated API request to NWO Robotics
 */
async function callAPI(endpoint, data) {
  validateConfig();
  
  const url = `${API_BASE}/${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY,
    'X-User-ID': USER_ID
  };
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(data)
    });
    
    if (response.status === 429) {
      throw new Error('API rate limit exceeded. Please upgrade your plan at https://nwo.capital/webapp/api-key.php');
    }
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.message || `API error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('NWO Robotics API Error:', error);
    throw error;
  }
}

/**
 * Main skill handler
 */
async function handle(input) {
  validateConfig();
  
  const sanitizedInput = sanitizeInput(input);
  
  if (!sanitizedInput) {
    return 'Please provide a command for the robots.';
  }
  
  const lowerInput = sanitizedInput.toLowerCase();
  
  // Parse command intent
  if (lowerInput.includes('status') || lowerInput.includes('state')) {
    return await getRobotStatus();
  }
  
  if (lowerInput.includes('stop') || lowerInput.includes('halt') || lowerInput.includes('emergency')) {
    return await emergencyStop();
  }
  
  if (lowerInput.includes('move') || lowerInput.includes('go to') || lowerInput.includes('navigate')) {
    return await handleMovement(sanitizedInput);
  }
  
  if (lowerInput.includes('scan') || lowerInput.includes('detect') || lowerInput.includes('find')) {
    return await handleVisionTask(sanitizedInput);
  }
  
  if (lowerInput.includes('temperature') || lowerInput.includes('sensor') || lowerInput.includes('iot')) {
    return await handleIoTQuery(sanitizedInput);
  }
  
  if (lowerInput.includes('patrol')) {
    return await handlePatrolMode(sanitizedInput);
  }
  
  // Default: treat as general task
  return await handleGeneralTask(sanitizedInput);
}

/**
 * Get status of all robots
 */
async function getRobotStatus() {
  try {
    const data = await callAPI('api-robotics.php', {
      action: 'get_agent_status',
      user_id: USER_ID
    });
    
    if (!data.agents || data.agents.length === 0) {
      return 'No robots currently connected. Check your robot connections and try again.';
    }
    
    const statusList = data.agents.map(agent => 
      `• ${agent.name || agent.id}: ${agent.status || 'unknown'}`
    ).join('\n');
    
    return `Robot Status:\n${statusList}`;
  } catch (error) {
    return `Error checking robot status: ${error.message}`;
  }
}

/**
 * Emergency stop all robots
 */
async function emergencyStop() {
  try {
    const data = await callAPI('api-safety.php', {
      action: 'emergency_stop',
      user_id: USER_ID
    });
    
    return '⚠️ Emergency stop activated. All robots halted.';
  } catch (error) {
    return `Error stopping robots: ${error.message}`;
  }
}

/**
 * Handle movement commands
 */
async function handleMovement(input) {
  try {
    // Extract robot ID and coordinates from input
    const robotMatch = input.match(/robot[_-]?(\w+)/i);
    const robotId = robotMatch ? robotMatch[1] : 'default';
    
    const coordMatch = input.match(/[xX]?:?\s*(\d+)[,\s]+[yY]?:?\s*(\d+)/);
    const coords = coordMatch ? { x: parseInt(coordMatch[1]), y: parseInt(coordMatch[2]) } : null;
    
    const data = await callAPI('api-robotics.php', {
      action: 'execute_task',
      task: 'navigation',
      robot_id: robotId,
      coordinates: coords,
      instruction: input
    });
    
    return `Command sent to robot ${robotId}. Status: ${data.status || 'pending'}`;
  } catch (error) {
    return `Error sending movement command: ${error.message}`;
  }
}

/**
 * Handle vision-based tasks
 */
async function handleVisionTask(input) {
  try {
    const data = await callAPI('api-perception.php', {
      action: 'detect_objects',
      query: input,
      user_id: USER_ID
    });
    
    if (!data.objects || data.objects.length === 0) {
      return 'No objects detected in the current view.';
    }
    
    const objects = data.objects.map(obj => 
      `• ${obj.label} (${obj.confidence}% confidence) at [${obj.x}, ${obj.y}]`
    ).join('\n');
    
    return `Detected ${data.objects.length} objects:\n${objects}`;
  } catch (error) {
    return `Error running vision task: ${error.message}`;
  }
}

/**
 * Handle IoT sensor queries
 */
async function handleIoTQuery(input) {
  try {
    const data = await callAPI('api-iot.php', {
      action: 'query_sensors',
      query: input,
      user_id: USER_ID
    });
    
    if (!data.sensors || data.sensors.length === 0) {
      return 'No sensor data available for the requested query.';
    }
    
    const readings = data.sensors.map(sensor => 
      `• ${sensor.location || sensor.id}: ${sensor.value}${sensor.unit || ''}`
    ).join('\n');
    
    return `Sensor Readings:\n${readings}`;
  } catch (error) {
    return `Error querying sensors: ${error.message}`;
  }
}

/**
 * Handle patrol mode
 */
async function handlePatrolMode(input) {
  const enable = !input.includes('off') && !input.includes('stop');
  
  try {
    const data = await callAPI('api-robotics.php', {
      action: 'set_behavior',
      behavior: 'patrol',
      enabled: enable,
      user_id: USER_ID
    });
    
    return enable ? 'Patrol mode activated.' : 'Patrol mode deactivated.';
  } catch (error) {
    return `Error setting patrol mode: ${error.message}`;
  }
}

/**
 * Handle general task requests
 */
async function handleGeneralTask(input) {
  try {
    const data = await callAPI('api-tasks.php', {
      action: 'plan_and_execute',
      instruction: input,
      user_id: USER_ID
    });
    
    return `Task submitted. ${data.message || 'Processing...'}`;
  } catch (error) {
    return `Error processing task: ${error.message}`;
  }
}

// Export for OpenClaw
module.exports = { handle };
