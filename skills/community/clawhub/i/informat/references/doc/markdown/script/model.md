# Model Definitions

## AI Assistant

### AiAgentContentMessage
AI Message
```ts
interface AiAgentContentMessage {
	type:string;// Type
	text:string;// Text
	imageUrl:string;// Image URL
}
```
### AiAgentThread
AI Thread
```ts
interface AiAgentThread {
	id:string;// ID
	companyId:string;// Team ID
	applicationId:string;// Application ID
	moduleId:string;// Module ID
	name:string;// Name
	isDebug:boolean;// Whether in debug mode
	rowNumber:number;// Sort order field
	createAccountId:string;// Creator ID
	createAccountAvatar:string;// Creator avatar
	createAccountName:string;// Creator name
	createTime:Date;// Creation time
	updateTime:Date;// Last update time
}
```
### AiAgentThreadMessage
AI Thread Message
```ts
interface AiAgentThreadMessage {
	id:number;// ID
	companyId:string;// Team ID
	applicationId:string;// Application ID
	moduleId:string;// Module ID
	threadId:string;// Thread ID
	messageId:string;// Message ID
	content:string;// Content
	toolCalls:string;// Tool calls
	role:string;// Role
	finishReason:string;// Finish reason
	promptTokens:number;// Prompt token count
	completionTokens:number;// Completion token count
	totalTokens:number;// Total token count
	startTime:Date;// Start time
	endTime:Date;// End time
	createTime:Date;// Creation time
	images:string;// Images
}
```
### OpenAIChatApproximate
AI Chat Approximate Location
```ts
interface OpenAIChatApproximate {
	city:string;// City name (free text input)
Example: "Beijing"
	country:string;// Country code (ISO 3166-1 two-letter standard)
Example: "CN" (China)
Validation suggestions:
1. Length must be 2 characters
2. Only uppercase letters allowed
	region:string;// Administrative region name (free text input)
Example: "Guangdong Province" or "California"
Note:
- Unlike province, may include smaller administrative units
	timezone:string;// Timezone configuration (IANA format)
Example: "Asia/Shanghai"
Typical values:
- China Standard Time: Asia/Shanghai
- Pacific Time: America/Los_Angeles
	longitude:Double;// Longitude (-180~180)
	latitude:Double;// Latitude (-90~90)
	radius:number;// Search radius (meters)
}
```
### OpenAIChatAudioOptions
AI Chat Message Audio Output Parameters
```ts
interface OpenAIChatAudioOptions {
	voice:string;// Voice type (e.g., alloy, ash, ballad, coral, echo, fable, nova, onyx, sage, shimmer)
	format:string;// Format (e.g., wav, mp3, flac, opus, pcm16)
}
```
### OpenAIChatMessage
AI Chat Message
```ts
interface OpenAIChatMessage {
	role:string;// Role (e.g., "system", "user", "assistant")
	content:object;// Message content (supports multiple formats)
Allowed types:
1. Plain text string
2. Content part array (currently only supports text type)
Examples:
- Simple text: "Hello, world"
- Multi-paragraph: [
  {"type":"text", "text":"First paragraph"},
  {"type":"text", "text":"Second paragraph"}
]
	tool_call_id:string;// Tool call ID
	name:string;// Role name (optional)
	tool_calls:object;// Tool call information (may be JSON structure)
	reasoning_content:object;// Reasoning process content
}
```
### OpenAIChatMessageContent
AI Chat Message Content
```ts
interface OpenAIChatMessageContent {
	text:string;// Text content
Format requirements:
- Non-empty string
- Length limit: 4096 characters
}
```
### OpenAIChatMessageSetting
AI Chat Message Setting
```ts
interface OpenAIChatMessageSetting {
	role:string;// Role
	content:object;// Content
}
```
### OpenAIChatPredictionOptions
AI Chat Message Prediction Output Configuration
```ts
interface OpenAIChatPredictionOptions {
	type:string;// Prediction content type (currently only supports 'content')
Required field
	content:object;// Static prediction content (should match model-generated content)
Format: string or array
Typical use cases:
- Regenerating code files (90% content unchanged)
- Template filling scenarios (only a few variables change)
Example:
content = "public class User {\n  private String id;\n"
}
```
### OpenAIChatReq
AI Chat Request
```ts
interface OpenAIChatReq {
	model:string;// Model ID, e.g., gpt-4o, determines generation capability and pricing
	messages:array<OpenAIChatMessage>;// Conversation message list (supports text/image/audio and other multimodal inputs)
	audio:OpenAIChatAudioOptions;// Audio output parameters, required when modalities includes audio
	frequency_penalty:double;// Frequency penalty value, between -2.0 and 2.0, positive values reduce repetitive content
	logit_bias:Map;// Token bias mapping table (token ID -> bias value -100~100). Adjusts generation probability of specific tokens: positive values increase probability (100 forces selection), negative values decrease probability (-100 forces exclusion). Example: to disable politically related words, set corresponding token IDs to -100
	logprobs:boolean;// Whether to return log probabilities of output tokens (use with top_logprobs). When true, returns log probability for each output token
	max_tokens:number;// Maximum number of tokens to generate (including visible output and reasoning tokens)
	max_completion_tokens:number;// Maximum number of tokens to generate (including visible output and reasoning tokens)
	metadata:Map;// Metadata key-value pairs (up to 16 pairs)
Technical specifications:
- Key: string (max 64 characters)
- Value: string (max 512 characters)
Typical use cases:
1. Request tracking (e.g., session_id)
2. Environment tagging (e.g., env=production)
3. Data classification (e.g., category=finance)
	modalities:array<String>;// Output type configuration (must match model capabilities)
Supported values:
- Text: ["text"] (default)
- Multimodal: ["text", "audio"]
Audio output requires configuring the audio parameter
	n:number;// Number of message options to generate (recommend keeping 1 to save cost)
	parallel_tool_calls:boolean;// Whether to enable parallel tool calls (default true)
When enabled, allows simultaneous execution of multiple tool calls
Applicable scenarios:
- Complex tasks requiring multiple API calls simultaneously
- When tool calls have no dependencies
Disable scenarios:
- Tool calls have strict ordering requirements
	prediction:OpenAIChatPredictionOptions;// Prediction output configuration (accelerates content regeneration)
Use when most of the response content is already known:
1. Document template filling (90% content unchanged)
2. Code file partial modification (function body unchanged)
3. Structured data updates (only some fields change)
Use with prediction_options configuration
	presence_penalty:double;// Topic novelty penalty, between -2.0 and 2.0, positive values increase likelihood of new topics
	response_format:OpenAIChatResponseFormatConfig;// Response format constraint configuration
Supported modes:
1. Default text: { type: "text" }
2. Legacy JSON: { type: "json_object" }
3. Structured JSON: { type: "json_schema", json_schema: {...} }
Recommend using json_schema mode first
	seed:number;// Deterministic generation seed (Beta feature)
Technical characteristics:
- Same seed + parameter combination will try to produce the same output
- Use with system_fingerprint to monitor backend changes
Use cases:
1. Result reproducibility testing (seed=123)
2. Keeping some parameters constant in A/B testing
Note: Minor differences may still occur
	service_tier:string;// Service tier configuration (default auto)
Options:
auto - Auto select (prioritize scale tier quota)
default - Basic service (no latency guarantee)
flex - Flexible processing (dedicated resource pool)
Response will include the actual service_tier used
	stop:object;// Stop sequences (up to 4), not applicable to o3/o4-mini and other latest reasoning models
	store:boolean;// Whether to store output (for model distillation)
	stream:boolean;// Whether to enable streaming, true for streaming output
	stream_options:OpenAIChatStreamOptions;// Streaming configuration options (only effective when stream=true)
Description:
- Controls streaming response data format
- Monitors real-time resource consumption
Typical configuration:
new StreamOptions().setIncludeUsage(true)
	temperature:double;// Sampling temperature (0-2), higher values produce more random output, recommend adjusting either this or top_p
	tool_choice:object;// Tool call strategy configuration
Supported formats:
1. String mode:
   - 'none': Disable tool calls
   - 'auto': Auto select (default)
   - 'required': Must call a tool
2. Object mode:
   {"type":"function","function":{"name":"get_weather"}}
	tools:array<OpenAIChatReqTool>;// Available tool list (currently only supports functions)
Technical specifications:
- Up to 128 functions
- Each tool must include a function definition
Typical use cases:
1. Data query API integration
2. Math calculation tool sets
3. Third-party service connectors
	top_logprobs:number;// Return top N possible tokens for each token position
Technical specifications:
- Value range: 0-20
- Use with logprobs=true
Example:
Setting 5 returns the top 5 tokens by probability for each position
Output structure includes:
- Token text
- Log probability value
- Offset information
	top_p:Double;// Nucleus sampling threshold (default 1.0)
How it works:
0.1 -> Only consider tokens in the top 10% probability mass
Typical configuration:
- Creative generation: 0.9
- Precise answers: 0.5
Note:
Adjust either this or temperature parameter
	user:string;// End user identifier
Description:
- Used for abuse behavior monitoring
- Supported format: mixed letters/numbers/special characters
Compliance requirements:
1. Must not contain PII information
2. Recommend using anonymous UUID
Example: "user_9FQ3Z"
	web_search_options:OpenAIChatWebSearchOptions;// Web search tool configuration
When enabled, the model will automatically search the internet for information
Typical use cases:
1. Real-time news queries
2. Localized information retrieval
3. Factual data verification
}
```
### OpenAIChatReqTool
AI Chat Request Tool Definition
```ts
interface OpenAIChatReqTool {
	type:string;// Tool type (fixed value 'function')
	function:OpenAIChatReqToolFunction;// Function detailed definition (name/description/parameter schema)
}
```
### OpenAIChatReqToolFunction
AI Chat Request Function Detailed Definition
```ts
interface OpenAIChatReqToolFunction {
	name:string;// Function name (must match [a-zA-Z0-9_-] format, max 64 characters)
Example: calculate_loan_payment
	description:string;// Function description (affects model's call decision)
Example: "Calculate monthly payment for commercial loan"
	parameters:object;// Parameter JSON Schema definition
Example: {"type":"object", "required":["amount"], 
"properties":{"amount":{"type":"number", "description":"Total loan amount"}}}
	strict_mode:boolean;// Strict mode (default false)
When enabled:
- Enforces parameter type checking
- Must provide required field
- Does not support complex constraints like regex
}
```
### OpenAIChatResp
AI Chat Response
```ts
interface OpenAIChatResp {
	choices:array<OpenAIChatRespChoices>;// Response option list (quantity determined by request parameter n)
Each option includes:
- Generated content
- Termination reason
- Index number
	created:number;// Response creation timestamp (Unix seconds)
Example: 1715751234 -> 2024-05-15 10:33:54
	id:string;// Response unique identifier (format: chatcmpl-XXXXXX)
Used for log tracking and auditing
	model:string;// Actual model identifier used
May differ from requested model (when auto-upgraded)
Example: gpt-4o-2024-05-13
	object:string;// Object type fixed value (chat.completion)
Used for response type identification
	service_tier:string;// Actual service tier used
Possible values: auto/default/flex
Used for billing analysis and performance monitoring
	system_fingerprint:string;// Backend configuration fingerprint (format: fp_xxxxxx)
Technical characteristics:
1. Identifies model runtime environment
2. Detects backend configuration changes
3. Works with seed parameter to ensure deterministic output
	usage:OpenAIChatRespUsage;// Token consumption statistics
	error:OpenAIChatRespError;// Error information
}
```
### OpenAIChatRespChoices
AI Chat Response Choice
```ts
interface OpenAIChatRespChoices {
	index:number;// Generation result index (starting from 0)
	message:OpenAIChatMessage;// Generated chat message
May contain multimodal content (text/audio)
	finish_reason:string;// Generation termination reason
Possible values:
stop - Normal termination
length - Reached token limit
tool_calls - Triggered tool call
}
```
### OpenAIChatRespCompletionTokensDetails
AI Token Usage Breakdown
```ts
interface OpenAIChatRespCompletionTokensDetails {
	accepted_prediction_tokens:number;// Number of tokens accepted from predicted output
Use case:
When using Predicted Outputs, the number of prediction content tokens actually adopted by the model
Example:
Prediction provides 100 tokens, 80 adopted -> accepted=80
	audio_tokens:number;// Tokens consumed for audio generation
Billing rule:
1 second of audio ≈ 50 tokens
Example:
Generating 30 seconds of speech -> approximately 1500 tokens
	reasoning_tokens:number;// Tokens consumed for reasoning process
Technical characteristics:
1. Reflects model's internal thinking process
2. Can be adjusted via reasoning_effort parameter
Optimization suggestion:
Setting to low for simple tasks can reduce reasoning tokens by 30%
	rejected_prediction_tokens:number;// Number of tokens rejected from predicted output
Billing note:
Still billed even though not adopted
Best practice:
Optimize prediction content match rate to reduce waste
}
```
### OpenAIChatRespError
AI API Call Error Information
```ts
interface OpenAIChatRespError {
	message:string;// Error message
	type:string;// Error type
	param:object;// Parameter
	code:string;// Error code
}
```
### OpenAIChatRespPromptTokensDetails
Input Prompt Token Usage Breakdown
```ts
interface OpenAIChatRespPromptTokensDetails {
	audio_tokens:number;// Audio input token count
Conversion rule:
1 second of audio ≈ 50 tokens
Example:
30 seconds of voice input -> approximately 1500 tokens
Billing note: Same rate as text tokens
	cached_tokens:number;// Cached reused token count
Technical characteristics:
1. From cache of similar historical requests
2. Not counted toward billed tokens
Optimization suggestion:
Repeated content requests can improve cache hit rate
}
```
### OpenAIChatRespTool
AI Chat Response ToolCall
```ts
interface OpenAIChatRespTool {
	id:string;// ID
	type:string;// Tool type (fixed value 'function')
	function:OpenAIChatRespToolFunction;// ToolCall function
}
```
### OpenAIChatRespToolFunction
AI Chat Response ToolCall Function
```ts
interface OpenAIChatRespToolFunction {
	name:string;// Function ID
	arguments:string;// Arguments
}
```
### OpenAIChatRespUsage
AI Token Consumption Statistics
```ts
interface OpenAIChatRespUsage {
	completion_tokens:number;// Tokens consumed for generated content
Includes:
- Text generation
- Audio/image generation (if multimodal enabled)
Billing basis: $0.002/thousand tokens (example)
	prompt_tokens:number;// Tokens consumed for input prompt
Calculation method:
(Text character count / 4) + multimodal content token surcharge
	total_tokens:number;// Total token consumption
Calculation rule:
prompt_tokens + completion_tokens
Monitoring suggestion:
Set threshold alerts (e.g., >4096 tokens per request)
	completion_tokens_details:OpenAIChatRespCompletionTokensDetails;// Generated content token usage details
Detailed breakdown:
- Text tokens
- Audio tokens (if enabled)
- Image tokens (if enabled)
Uses:
1. Multimodal cost analysis
2. Generated content optimization
	prompt_tokens_details:OpenAIChatRespPromptTokensDetails;// Input prompt token details
}
```
### OpenAIChatResponseFormatConfig
AI Chat Message Helper Configuration Class
```ts
interface OpenAIChatResponseFormatConfig {
	type:string;// Format type (required)
Options: text/json_object/json_schema
	json_schema:object;// JSON Schema definition (required when type=json_schema)
Example: {"type":"object","properties":{"name":{"type":"string"}}}
}
```
### OpenAIChatSetting
AI Chat Configuration
```ts
interface OpenAIChatSetting {
	url:string;// OpenAI API request URL, default is https://api.openai.com/v1/chat/completions
	model:string;// GPT model to use, default is gpt-4o
	apiKey:string;// OpenAI API key
	temperature:double;// Sampling temperature, higher values produce more random output, default is 1
	topp:double;// Top-p sampling (nucleus sampling) parameter, default is 1
	timeout:number;// Timeout (seconds), default is 0
	presencePenalty:double;// Topic novelty penalty, default is 0
	frequencyPenalty:double;// Frequency penalty to prevent repetitive content, default is 0
	maxTokens:number;// Maximum number of tokens to generate, default is 0
	n:number;// Number of responses to generate, default is 1
	stop:string;// Stop words (generation stops when encountering these words, separate multiple stop words with commas. Maximum 4)
	messages:array<OpenAIChatMessageSetting>;// Content to send
	extra_body:object;// Extra information
}
```
### OpenAIChatStreamOptions
AI Chat Message Streaming Configuration Options
```ts
interface OpenAIChatStreamOptions {
	include_usage:boolean;// Whether to include usage statistics
When enabled:
1. Sends final statistics block before stream ends
2. Each data chunk contains an empty usage field
Note:
- Final statistics may be lost if stream is interrupted
}
```
### OpenAIChatToolChoice
AI Chat Tool Call Strategy Configuration (object mode)
```ts
interface OpenAIChatToolChoice {
	type:string;// Tool type (currently only supports function)
	function:OpenAIChatToolChoiceFunction;// Function detailed definition
}
```
### OpenAIChatToolChoiceFunction
AI Chat Tool Call Strategy Configuration Function Definition
```ts
interface OpenAIChatToolChoiceFunction {
	name:string;// Function name (must follow naming conventions)
Example: get_current_weather
}
```
### OpenAIChatUserLocation
AI Chat Approximate Location Configuration
```ts
interface OpenAIChatUserLocation {
	approximate:OpenAIChatApproximate;// Approximate location parameters (required)
	type:string;// Type of location approximation. Always "approximate"
}
```
### OpenAIChatWebSearchOptions
AI Chat Message Web Search Configuration
```ts
interface OpenAIChatWebSearchOptions {
	search_context_size:string;// Search context window size (default medium)
Options:
- low: Compact context (approximately 500 tokens)
- medium: Balanced mode (approximately 1500 tokens)
- high: Extended context (approximately 3000 tokens)
	user_location:OpenAIChatUserLocation;// Approximate location configuration
Used for location-relevant searches
Example: Set user's city range
}
```
## Application

### Account
Account
```ts
interface Account {
	id:string;// ID
	name:string;// Name
	avatar:string;// Avatar
	userName:string;// Username
	mobileNo:string;// Mobile number
	email:string;// Email
	companyId:string;// Team ID
	companyList:string;// Team ID list
	oid:string;// Third-party ID
	createTime:Date;// Creation time
	updateTime:Date;// Last update time
	lastLoginTime:Date;// Last login time
	language:string;// Language
	needUpdatePassword:boolean;// Whether password reset is needed
	isValid:boolean;// Whether valid
}
```
### AccountAddForm
Add Account
```ts
interface AccountAddForm {
	id:string;// Account ID
	name:string;// Name
	userName:string;// Username
	mobileNo:string;// Mobile number
	email:string;// Email
	password:string;// Password
	oid:string;// Third-party ID
	avatar:string;// Avatar
	remark:string;// Remark
	needUpdatePassword:boolean;// Whether password reset is needed
}
```
### AccountToken
Account Login Credential
```ts
interface AccountToken {
	type:string;// Type
	accountId:string;// Account ID
	companyId:string;// Team ID
	token:string;// Credential
	expireTime:Date;// Expiration time
	createTime:Date;// Creation time
	dbIndex:number;// Database index
}
```
### App
Application
```ts
interface App {
	id:string;// ID
	name:string;// Name
	icon:string;// Icon
	color:string;// Color
	appDefineId:string;// Application identifier
	logLevel:string;// Log level
	env:string;// Runtime environment
	enableAppLog:boolean;// Whether to output logs to file (text)
	enableAppJsonLog:boolean;// Whether to output logs to file (JSON)
	appDefineBuild:number;// Publish build number
	appDefineVersion:string;// Application version
	appDefineEditable:boolean;// Whether application design is allowed
	groupId:string;// Group
	createAccountId:string;// Creator
	updateAccountId:string;// Updater
	createTime:Date;// Creation time
	updateTime:Date;// Last update time
}
```
### AppChangeLog
Application Operation Log
```ts
interface AppChangeLog {
	id:string;// ID
	type:string;// Type
	content:string;// Content
	createAccountId:string;// Creator
	createAccountAvatar:string;// Creator avatar
	createAccountName:string;// Creator name
	createTime:Date;// Creation time
}
```
### AppDefine
Application Configuration
```ts
interface AppDefine {
	id:string;// ID
	name:string;// Name
	color:string;// Color
	roleList:array<ObjectRef>;// Role list
	moduleList:array<ObjectRef>;// Module list
	automaticList:array<ObjectRef>;// Automation list
	scriptList:array<ObjectRef>;// Script list
	scheduleList:array<ObjectRef>;// Scheduled task list
	apiList:array<ObjectRef>;// API list
	versionList:array<ObjectRef>;// Version list
	eventList:array<AppEventDefine>;// Event list
}
```
### AppEvent
Application Event
```ts
interface AppEvent {
	id:string;// ID
	content:object;// Content
}
```
### AppEventDefine
Application Event Definition
```ts
interface AppEventDefine {
	id:string;// ID
	key:string;// Identifier
	name:string;// Name
	remark:string;// Remark
}
```
### ApplicationProcess
Application Process
```ts
interface ApplicationProcess {
	id:string;// ID
	type:string;// Type
	associatedId:string;// Associated ID
	associatedName:string;// Associated name
	associatedKey:string;// Associated identifier
	startTime:Date;// Start time
	endTime:Date;// End time
	status:string;// Status
	serverId:string;// Server ID
}
```
### CustomRole
Application Custom Role
```ts
interface CustomRole {
	id:string;// ID
	name:string;// Name
	remark:string;// Remark
	permissionList:array<String>;// Permission list
	createTime:Date;// Creation time
	updateTime:Date;// Last update time
}
```
### ModuleAlert
Module Alert
```ts
interface ModuleAlert {
	moduleId:string;// Module identifier
	title:string;// Alert title
	description:string;// Alert description
	closeable:boolean;// Whether closeable
	modal:boolean;// Whether to display as modal
	center:boolean;// Whether to center display
	descriptionHtml:boolean;// Whether the description field uses HTML format
	showIcon:boolean;// Whether to show icon
	type:string;// Alert type, options: success, warning, info, error
}
```
### ModuleFavorite
My Favorites
```ts
interface ModuleFavorite {
	id:string;// ID
	accountId:string;// Account ID
	applicationId:string;// Application ID
	moduleId:string;// Module ID
	moduleName:string;// Module name
	moduleType:string;// Module type
	moduleIcon:string;// Module icon
}
```
### ObjectRef
Object Reference
```ts
interface ObjectRef {
	id:string;// ID
	key:string;// Identifier
	name:string;// Name
	icon:string;// Icon
	type:string;// Type
	remark:string;// Remark
	isDirectory:boolean;// Whether directory
	children:array<ObjectRef>;// Child nodes
	expand:boolean;// Expanded
	displayName:string;// Display name
}
```
### PushEvent
Push Event
```ts
interface PushEvent {
	eventId:string;// Event ID: ModuleRefresh - Refresh module, RecordFormRefresh - Refresh record form, Toast - Show toast message
	moduleRefreshModuleId:string;// Module identifier to refresh
	recordFormRefreshTableId:string;// Data table identifier of the record form to refresh
	recordFormRefreshRecordId:string;// Record ID of the record form to refresh
	toastMessage:string;// Toast message content
	recordFormCloseTableId:string;// Data table of the record
	recordFormCloseRecordId:string;// Record form record ID
	scriptContent:string;//
	scriptVarList:array<Object>;//
	sendType:string;// Push type: currentUser - Current user, allCompanyMember - All team members, allApplicationMember - All application members, specificUser - Specific user
	accountIdList:array<String>;// Only effective when push type is specific user
}
```
### ScriptDefine
Script
```ts
interface ScriptDefine {
	id:string;// ID
	name:string;// Name
}
```
## Automation

### FormContent
Event Content
```ts
interface FormContent {
	formRecord:Map;// Form data, returned when event type is form.field.change or form.init
	formFieldId:string;// Changed field ID, returned when event type is form.field.change or form.init
	record:Map;// Clicked record data, returned when event type is record.dblclick or record.click
	field:string;// Clicked field, returned when event type is record.dblclick or record.click
	date:number;// Timestamp of clicked date, returned when event type is calendar.datedblclick
	pageIndex:number;// Current page number, returned when event type is table.loaded
	pageSize:number;// Page size, returned when event type is table.loaded
	tableViewCondition:number;// Query condition, returned when event type is table.loaded
	queryFilterKey:number;// Combined filter identifier used, returned when event type is table.loaded
	type:number;// Trigger type: view.setup - After view initialization; view.reload - After view internally requests data reload; view.page.change - After view pagination info changes; view.fullpath.change - After view tree structure full path display toggle; view.orderby.change - After non-table view adjusts sorting; view.inner.query.change - After view internally changes query conditions (calendar view); view.query.change - After view filter query conditions; view.filter.change - After view combined filter switch; view.root.change - After view tree structure sets query root node; record.create.refresh - Refresh after record creation; record.update.refresh - Refresh after record update; record.delete.refresh - Refresh after record deletion; record.parent.change - Refresh after record parent change; automatic.output.refresh - Automation interaction set module refresh; automatic.output.set.filter - Automation interaction set view filter condition; automatic.output.set.root - Automation set view data root node, returned when event type is record.dblclick
	platform:number;// Platform of the accessing device: web, mobile, returned when event type is table.loaded
	moduleKey:number;// Module identifier, returned when event type is table.loaded
}
```
### FormEvent
Form Event
```ts
interface FormEvent {
	id:string;// Event type, options: Form field change - form.field.change, Form initialization - form.init
	tableId:string;// Data table ID
	content:FormContent;// Event content
}
```
### RecordFormCloseEvent
Data Table Form Close Event
```ts
interface RecordFormCloseEvent {
	record:Map;// Form data
	list:array;// Custom table row data (selected or all)
	formModuleKey:string;// Data table form identifier
	type:string;// Form type
RecordCreateForm: Data table record creation form
RecordInfoForm: Data table record detail form
OutputDynamicForm: Automation custom form
OutputDynamicTable: Automation custom table
}
```
### TableQueryEvent
Data Table Query Event
```ts
interface TableQueryEvent {
	type:string;// Event type, options: Before query - table.query.before, After query - table.query.after
	tableId:string;// Identifier of the queried data table
	moduleId:string;// Queried module ID
	condition:Query;// Query condition
	list:array;// Queried record list
	count:number;// Total queried record count
}
```
### ViewCondition
Data Table Query Condition
```ts
interface ViewCondition {
	pageIndex:number;// Current page number
	pageSize:number;// Page size
	childrenRootRecordId:string;// Root node ID for tree structure query
	childrenFieldId:string;// Field for tree structure query
	filter:ViewFilter;// Filter condition
	orderByList:array<String>;// Sort fields
}
```
### ViewEvent
Data Table View Event
```ts
interface ViewEvent {
	id:string;// Event type, options: Double-click record - record.dblclick, Single-click record - record.click, Calendar view double-click blank date - calendar.datedblclick, After view data loaded - table.loaded
	moduleId:string;// Module ID
	content:FormContent;// Event content
}
```
### ViewFilter
Data Table Filter
```ts
interface ViewFilter {
	opt:string;// Operator: and, or
	conditionList:array<String>;// Filter field list
}
```
## Workflow

### BpmnComment
Workflow Comment
```ts
interface BpmnComment {
	id:string;// Comment ID
	createTime:Date;// Creation time
	userId:string;// User ID
	taskId:string;// Task ID
	procInstId:string;// Process instance ID
	message:string;// Message
	type:string;// Type
}
```
### BpmnCommentQuery
Workflow Comment Query
```ts
interface BpmnCommentQuery {
	procInstId:string;// Process instance ID
	taskId:string;// Task ID
	executionId:string;// Execution ID
	filter:Filter;// Filter
	pageIndex:number;// Page number, default: 1
	pageSize:number;// Page size, default: 50
	orderByList:array<OrderBy>;// Sort order
	includeFields:LinkedHashSet;// Return field list
	excludeFields:Set;// Exclude field list
}
```
### BpmnFlow
Workflow Sequence Flow
```ts
interface BpmnFlow {
	id:string;// ID
	name:string;// Name
	sourceRef:string;// Source node
	targetRef:string;// Target node
	conditionExpression:string;// Condition expression
	remark:string;// Remark
}
```
### BpmnIdentityLink
Workflow Identity Link
```ts
interface BpmnIdentityLink {
	id:string;// Unique identifier of the IdentityLink
	type:string;// Type of the IdentityLink, typically participant or candidate
	userId:string;// User ID associated with the IdentityLink
	groupId:string;// User role ID associated with the IdentityLink
	taskId:string;// Workflow task ID
}
```
### BpmnInstance
Workflow Instance
```ts
interface BpmnInstance {
	id:string;// ID
	name:string;// Instance name
	procInstId:string;// Workflow instance ID
	businessKey:string;// Business key
	procDefId:string;// Workflow definition ID
	isActive:boolean;// Whether active
	startTime:Date;// Start time
	endTime:Date;// End time
	taskCount:number;// Task count
	startUserId:string;// Initiator
	startUserName:string;// Initiator name
	startUserAvatar:string;// Initiator avatar
	procDefName:string;// Workflow definition name
	tenantId:string;// Application ID and module ID
	deleteReason:string;// Cancellation reason
}
```
### BpmnInstanceQuery
Workflow Instance Query
```ts
interface BpmnInstanceQuery {
	status:string;// Instance status: In progress - doing, Completed - done
	processDefineId:string;// Workflow definition identifier
	name:string;// Instance name
	startUserId:string;// Initiator ID
	startUserIdInList:array<String>;// Initiator ID list
	startTimeStart:Date;// Start time begin
	startTimeEnd:Date;// Start time end
	endTimeStart:Date;// End time begin
	endTimeEnd:Date;// End time end
	varList:array<BpmnVar>;// Workflow variable list
	businessKey:string;// businessKey
	idList:array<String>;// ID list
	filter:Filter;// Filter
	pageIndex:number;// Page number, default: 1
	pageSize:number;// Page size, default: 50
	orderByList:array<OrderBy>;// Sort order
	includeFields:LinkedHashSet;// Return field list
	excludeFields:Set;// Exclude field list
}
```
### BpmnNode
Workflow Node
```ts
interface BpmnNode {
	id:string;// ID
	name:string;// Node name
	type:string;// Node type
	remark:string;// Node remark
	taskSetting:BpmnTaskSetting;// Node task configuration
}
```
### BpmnProcess
Workflow Definition
```ts
interface BpmnProcess {
	id:string;// Process ID
	defineId:string;// Process definition ID
	key:string;// Identifier
	name:string;// Name
	icon:string;// Icon
	remark:string;// Description
	color:string;// Color identifier
	rowNumber:number;// Sort order
	createTime:Date;// Creation time
	updateTime:Date;// Last modified time
}
```
### BpmnProcessDiagramConfig
Workflow Process Diagram
```ts
interface BpmnProcessDiagramConfig {
	imageType:string;// Image type, default png
	highLightedActivities:array<String>;// Completed process tasks
	highLightedFlows:array<String>;// Completed sequence flows
	activityFontName:string;// Process task font name
	labelFontName:string;// Label font name
	annotationFontName:string;// Annotation font name
	scaleFactor:double;// Scale factor
	drawSequenceFlowNameWithNoLabelDI:boolean;//
}
```
### BpmnProcessQuery
Workflow Definition Query
```ts
interface BpmnProcessQuery {
	accountId:string;// Account ID that can initiate the process
	name:string;// Workflow name
	filter:Filter;// Filter
	pageIndex:number;// Page number, default: 1
	pageSize:number;// Page size, default: 50
	orderByList:array<OrderBy>;// Sort order
	includeFields:LinkedHashSet;// Return field list
	excludeFields:Set;// Exclude field list
}
```
### BpmnProcessXml
Workflow XML Parsed Object
```ts
interface BpmnProcessXml {
	id:string;// ID
	name:string;// Process name
	startSetting:BpmnStartSetting;// Process start configuration
	nodeList:array<BpmnNode>;// Process node list
	flowList:array<BpmnFlow>;// Process sequence flow list
}
```
### BpmnStartSetting
Process Definition Start Setting
```ts
interface BpmnStartSetting {
	instanceNameVar:string;//
	draftNameVar:string;//
	enableStartForm:boolean;//
	formSetting:FormSetting;//
	startFormToolbarButtonList:array<Button>;//
	instanceToolbarButtonList:array<Button>;//
	startVarList:array<BpmnFormSettingVar>;//
	activityUserList:array<NodeUser>;//
}
```
### BpmnTableFieldSetting
Process Form Field Definition
```ts
interface BpmnTableFieldSetting {
	id:string;//
	editable:boolean;//
	visible:boolean;//
	defaultValue:object;//
}
```
### BpmnTask
Workflow Task
```ts
interface BpmnTask {
	id:string;// ID
	name:string;// Instance name
	procDefId:string;// Workflow definition ID
	procDefName:string;// Workflow definition name
	procInstId:string;// Workflow instance ID
	procInstName:string;// Workflow instance name
	taskDefKey:string;// Task definition key
	executionId:string;// Task execution ID
	tenantId:string;// Application ID and module ID
	assignee:string;// Assignee ID
	assigneeName:string;// Assignee name
	assigneeAvatar:string;// Assignee avatar
	delegation:string;// Delegation status: PENDING - Task assignee delegated, RESOLVED - Delegatee has resolved the task
	owner:string;// Delegator or transferor
	ownerName:string;// Delegator or transferor name
	ownerAvatar:string;// Delegator or transferor avatar
	startUserId:string;// Initiator
	startUserName:string;// Initiator name
	startUserAvatar:string;// Initiator avatar
	dueDate:Date;// Due date
	claimTime:Date;// Claim or assign time
	startTime:Date;// Start time
	endTime:Date;// Completion time
	duration:number;// Duration
	deleteReason:string;// Cancellation reason
	lastUpdatedTime:Date;// Last updated time
}
```
### BpmnTaskCc
Workflow Task CC (Carbon Copy)
```ts
interface BpmnTaskCc {
	id:string;// ID
	taskId:string;// Task ID
	copyUserId:string;// CC user
	startUserId:string;// Initiator
	copyUserAvatar:string;// CC user avatar
	copyUserName:string;// CC user name
}
```
### BpmnTaskQuery
Workflow Task Query
```ts
interface BpmnTaskQuery {
	accountId:string;// Assignee account ID
	status:string;// Status: In progress - doing, Completed - done
	assignee:string;// Assignee type: All - all, Assigned to me - assignee, Pending claim - candidate, CC to me - copy
	taskName:string;// Task name
	procInstId:string;// Process ID
	createTimeStart:Date;// Creation time begin
	createTimeEnd:Date;// Creation time end
	executionId:string;// Task execution ID
	filter:Filter;// Filter
	pageIndex:number;// Page number, default: 1
	pageSize:number;// Page size, default: 50
	orderByList:array<OrderBy>;// Sort order
	includeFields:LinkedHashSet;// Return field list
	excludeFields:Set;// Exclude field list
	taskDefKey:string;// taskDefKey
	dueDateStart:Date;// Due date start
	dueDateEnd:Date;// Due date end
}
```
### BpmnVar
Workflow Variable
```ts
interface BpmnVar {
	name:string;// Variable name
	value:object;// Value
	opt:string;//
}
```
### FormSetting
Process Form Setting
```ts
interface FormSetting {
	id:string;//
	tableId:string;//
	tableFieldSettingList:array<BpmnTableFieldSetting>;//
	toolBarButtonList:array<Button>;//
	localVariable:boolean;//
	completeSetVarList:array<CompleteSetVar>;//
	enableShowProcessInfo:boolean;//
	formType:string;//
	formDesignerModuleId:string;//
	formDesignerFormId:string;//
	formDesignerFieldSettingList:array<BpmnTableFieldSetting>;//
}
```
## Team

### AppGroup
Application Group
```ts
interface AppGroup {
	id:string;// ID
	name:string;// Name
	rowNumber:number;// Sort order
	createTime:Date;// Creation time
	updateTime:Date;// Last update time
}
```
### Company
Team
```ts
interface Company {
	id:string;// ID
	name:string;// Name
	dbIndex:number;// Database index
	avatar:string;// Team logo
	favicon:string;// Browser icon
	version:string;// Current plan
	createAccountId:string;// Creator
	maxUserNum:number;//
	maxApplicationNum:number;//
	createTime:Date;// Creation time
	updateTime:Date;// Last update time
	isValid:boolean;// Status
	memberNum:number;// Current member count
}
```
### CompanyMember
Team Member
```ts
interface CompanyMember {
	id:string;// Account ID
	name:string;// Account name
	leaderList:array<String>;// Direct supervisor list
	roleList:array<String>;// Role list
	departmentList:array<String>;// Department list
	departmentKeyList:array<String>;// Department identifier list
	dingtalkUserId:string;// DingTalk account ID
	weworkUserId:string;// WeCom account ID
	feishuUserId:string;// Feishu account ID
	rowNumber:number;// Sort weight
	createTime:Date;// Creation time
	updateTime:Date;// Last update time
}
```
### CompanyRole
Team Role
```ts
interface CompanyRole {
	id:string;// Identifier
	name:string;// Name
	isAdmin:boolean;// Whether administrator
	permissionIds:Set;// Permission list
	createTime:Date;// Creation time
}
```
### InstallAppRequest
Install Application Request
```ts
interface InstallAppRequest {
	imrUrl:string;// IMR file URL
	groupId:string;// Group ID
	isForce:boolean;// Whether to force
}
```
### OptLog
Operation Log
```ts
interface OptLog {
	id:string;// ID
	name:string;// Name
	accountId:string;// Operating account ID
	accountName:string;// Operating account name
	accountAvatar:string;// Operating account avatar
	companyId:string;// Team ID
	companyName:string;// Team name
	associatedId:string;// Associated ID
	type:string;// Type
	remark:string;// Remark
	ip:string;// IP
	createTime:Date;// Creation time
	updateTime:Date;// Update time
}
```
### UpdateAppGroupRequest
Update Application Group Request
```ts
interface UpdateAppGroupRequest {
	imrUrl:string;// IMR file URL
	groupId:string;// Group ID
}
```
### UpgradeAppRequest
Upgrade Application Request
```ts
interface UpgradeAppRequest {
	appId:string;// Application ID
	imrUrl:string;// IMR file URL
	isForce:boolean;// Whether to force
}
```
### UserAppList
Application List
```ts
interface UserAppList {
	appList:array<App>;//
	appGroupList:array<AppGroup>;//
}
```
## Data Source

### DataSourceConnnectionSetting
Data Source Configuration
```ts
interface DataSourceConnnectionSetting {
	autoCommit:boolean;// Whether to auto-commit transactions, default is true
}
```
## Department

### Department
Department
```ts
interface Department {
	id:string;// ID
	name:string;// Department name
	shortName:string;// Short name
	remark:string;// Description
	parentId:string;// Parent department ID
	ownerList:array<String>;// Owner list
	rowNumber:number;// Sort order
	isDisable:boolean;// Whether disabled
}
```
## Application Design

### RefEntity
Reference Relationship
```ts
interface RefEntity {
	scope:string;//
	id:string;//
	type:string;//
	name:string;//
	key:string;//
	className:string;//
	isEntity:boolean;//
	children:array<RefEntity>;//
	relations:array<RefEntityRelation>;//
}
```
### RefEntityRelation
Reference Object
```ts
interface RefEntityRelation {
	parent:string;//
	to:string;//
	type:string;//
	relation:string;//
}
```
### DefineObject
Application Design Model
```ts
interface DefineObject {
	id:string;// ID
	key:string;// Identifier
	scope:string;// Scope
	name:string;// Name
	displayName:string;// Display name
	remark:string;// Remark
	build:number;//
	draftVersion:number;//
	isDeleted:boolean;//
	parentId:string;//
	parentName:string;//
	createUser:string;//
	updateUser:string;//
	createTime:string;//
	updateTime:string;//
}
```
### DefineObjectQuery
DefineObject Query Object
```ts
interface DefineObjectQuery {
	name:string;// Name
	key:string;// Key
	type:string;// Type
	scope:string;// Scope
	pageIndex:number;// Page number, default: 1
	pageSize:number;// Page size, default: 50
}
```
### ScriptDefine
Application Script Definition
```ts
interface ScriptDefine {
	content:string;// Content
	id:string;// ID
	key:string;// Identifier
	scope:string;// Scope
	name:string;// Name
	displayName:string;// Display name
	remark:string;// Remark
	build:number;//
	draftVersion:number;//
	isDeleted:boolean;//
	parentId:string;//
	parentName:string;//
	createUser:string;//
	updateUser:string;//
	createTime:string;//
	updateTime:string;//
}
```
### TableFieldDefineSimple
Data Table Field Definition
```ts
interface TableFieldDefineSimple {
	id:string;// ID
	name:string;// Name
	key:string;// Identifier
	scope:string;// Scope
	type:string;// Type
}
```
## Email

### EmailRecipient
Email Recipient
```ts
interface EmailRecipient {
	address:string;// Address
	personal:string;// Name
	type:string;// Send type
}
```
### EmailServer
Email Server
```ts
interface EmailServer {
	host:string;// Host
	port:number;// Port
	ssl:boolean;// Whether to enable SSL
	auth:boolean;// Whether to enable authentication
	account:string;// Account
	password:string;// Password
	protocol:string;// Protocol
}
```
## Excel

### TemplateCell
Cell Template
```ts
interface TemplateCell {
	content:object;// Cell value
	rowspan:number;//
	colspan:number;//
}
```
## File

### File
File
```ts
interface File {
	name:string;// File name
	path:string;// File path
	absolutePath:string;// Absolute path
	isAbsolute:boolean;// Whether absolute path is enabled
	canRead:boolean;// Whether readable
	canWrite:boolean;// Whether editable
	isDirectory:boolean;// Whether directory
	isFile:boolean;// Whether file
	totalSpace:number;// File size
	usableSpace:number;// Usable space
	lastModified:number;// Last modified time
	length:number;// Length
}
```
## FTP

### FtpFile
File Transfer
```ts
interface FtpFile {
	group:string;// File group
	hardLinkCount:number;// Link count
	link:string;// Link
	name:string;// File name
	size:number;// File size
	timestamp:Calendar;// Last modified timestamp
	timestampInstant:Instant;// Instant timestamp
	type:number;// File type
	user:string;// File owner
	directory:boolean;// Whether directory
	file:boolean;// Whether file
}
```
## Http

### HttpRequest
HTTP Request
```ts
interface HttpRequest {
	url:string;// Request URL
	method:string;// Request method
	timeout:number;// Timeout in milliseconds
	body:string;// Request body
	charset:string;// Character set
	followRedirect:boolean;//
	maxRedirectCount:number;// Redirect count
	headers:Map;// Request headers
	overrideHeaders:Map;// Override headers
	form:Map;// Request form
	files:Map;// Request files
	storages:Map;//
	bodyBytes:byte[];// Byte array request body
}
```
## Jdbc

### ConnnectionInfo
Database Connection
```ts
interface ConnnectionInfo {
	dburl:string;// Database connection string
	dbuser:string;// Username
	dbpassword:string;// Password
	driverClassName:string;// Driver name
	autoCommit:boolean;// Whether to auto-commit transactions, default is true
}
```
### JDBCResultSet
JDBC Result Set
```ts
interface JDBCResultSet {
	rs:ResultSet;// Result set
}
```
## Ldap

### LdapConnectionInfo
LDAP Connection
```ts
interface LdapConnectionInfo {
	initialContextFactory:string;// Context service provider
	providerURL:string;// Server address
	securityAuthentication:string;// Authentication method: none - No authentication, simple - Username/password authentication
	securityPrincipal:string;// Username
	securityCredentials:string;// Password
	referral:string;// Server address
}
```
### LdapListResult
LDAP List Result
```ts
interface LdapListResult {
	className:string;//
	name:string;//
	nameInNamespace:string;//
	isRelative:boolean;//
}
```
### LdapModifyAttribute
LDAP Attribute List
```ts
interface LdapModifyAttribute {
	id:string;// Attribute ID
	value:object;// Attribute value
}
```
### LdapSearchControl
Search Control
```ts
interface LdapSearchControl {
	returningAttributes:String[];// Returning attribute list
	searchScope:string;// Search scope, default is SUBTREE. SUBTREE - Returns all matching entries, ONELEVEL - Returns entries at the same level, OBJECT - Returns only matching objects
	countLimit:number;// Maximum number of entries to return
	timeLimit:number;// Connection timeout in milliseconds
	returningObjFlag:boolean;// Whether to return objects
	derefLinkFlag:boolean;// JNDI links are dereferenced during
}
```
### LdapSearchResult
LDAP Search Result
```ts
interface LdapSearchResult {
	className:string;//
	name:string;// Entry name
	nameInNamespace:string;// Full path of the entry
	object:object;//
	attributes:array<LdapSearchResultAttribute>;// Entry attribute list
}
```
### LdapSearchResultAttribute
LDAP Entry Attribute
```ts
interface LdapSearchResultAttribute {
	id:string;// Attribute ID
	values:Object[];// Attribute value list
}
```
## Mpp

### MppCustomFieldValueDataType
Custom Field Data Type
```ts
interface MppCustomFieldValueDataType {
	value:number;// Value
	maskValue:number;// Mask
	dataType:string;// Data type
}
```
### MppCustomFieldValueMask
MPP Custom Field Mask
```ts
interface MppCustomFieldValueMask {
	length:number;// Length
	level:number;// Level
	separator:string;// Separator
	type:MppCustomFieldValueDataType;//
}
```
### MppWriterConfig
MPP Configuration File
```ts
interface MppWriterConfig {
	microsoftProjectCompatibleOutput:boolean;// Whether the output can be read by MS Project, default is true
	splitTimephasedAsDays:boolean;// Controls whether to split timephased assignment data into days. Default is true
	writeTimephasedData:boolean;// Controls whether to write timephased resource assignment data to the file. Default is false
	saveVersion:string;// Sets the save version to use when generating MSPDI files, default is Project2016
}
```
## Message Queue

### MqMessage
Message Queue Message
```ts
interface MqMessage {
	body:object;// Message body
	props:MqMessageProperties;// Message properties
}
```
### MqMessageProperties
Message Properties
```ts
interface MqMessageProperties {
	headers:Map;// Message headers
	timestamp:Date;// Message timestamp, the time the message was generated
	messageId:string;// Message ID
	userId:string;// Sending user
	appId:string;// Sending application ID
	clusterId:string;// Cluster ID
	type:string;// Message type
	correlationId:string;// ID for correlating requests and responses
	replyTo:string;// Specifies the queue name for receiving responses
	contentType:string;// MIME type of message content
	contentEncoding:string;// Encoding of message content
	contentLength:number;// Message content length
	deliveryMode:string;// Message persistence: 2 for persistent, 1 for non-persistent
	expiration:string;// Message expiration time in milliseconds
	priority:number;// Message priority, higher values mean higher priority
	redelivered:boolean;// Whether already delivered
	receivedExchange:string;// Received exchange
	receivedRoutingKey:string;// Received routing key
	receivedUserId:string;// Received user
	deliveryTag:number;// Delivery tag
	messageCount:number;// Message count
	consumerTag:string;// Consumer tag
	consumerQueue:string;// Consumer queue
	receivedDelay:number;// Received delay
	receivedDeliveryMode:string;// Received delivery mode
	finalRetryForMessageWithNoId:boolean;// Final retry
	publishSequenceNumber:number;// Publish sequence number
	lastInBatch:boolean;// Whether last in batch
	projectionUsed:boolean;// Projection
}
```
### MqPublishSetting
Message Publish Setting
```ts
interface MqPublishSetting {
	expiration:number;// Time to live, unit: milliseconds
	priority:number;// Priority
	deliveryMode:number;// Delivery mode
	waitForConfirms:boolean;// Whether to wait for confirmation
}
```
## Notification

### Notification
Notification
```ts
interface Notification {
	id:string;// System notification ID
	accountId:string;// Account ID
	companyId:string;// Team ID
	applicationId:string;// Application ID
	name:string;// Notification title
	type:string;// Type: openbpmntask - Open BPMN task, openurl - Open URL, openrecord - Open data table record
	content:string;// Notification content
	data:string;// Additional information corresponding to the type
	isRead:boolean;// Whether read
	isWebSend:boolean;// Whether sent via web
	isWeworkSend:boolean;// Whether sent via WeCom
	isDingTalkSend:boolean;// Whether sent via DingTalk
	isFeishuSend:boolean;// Whether sent via Feishu
	isCustomSend:boolean;// Whether sent via custom notification
	createTime:Date;// Creation time
	updateTime:Date;// Update time
}
```
### NotificationAutomaticSetting
Automation Invocation Configuration
```ts
interface NotificationAutomaticSetting {
	automaticId:string;// Automation ID
	args:array<Object>;// Parameter list
}
```
### NotificationBpmnTaskSetting
Workflow Task Configuration
```ts
interface NotificationBpmnTaskSetting {
	taskId:string;// Task ID
	moduleId:string;// Module ID
}
```
### NotificationForm
System Notification Form
```ts
interface NotificationForm {
	title:string;// Title
	content:string;// Content
	accountId:string;// Account ID
	type:string;// Type: openbpmntask - Open BPMN task, openurl - Open URL, openrecord - Open data table record
	name:string;//
	urlSetting:NotificationUrlSetting;// URL configuration. Effective when type is openurl
	recordSetting:NotificationReocrdSetting;// Data table record configuration. Effective when type is openrecord
	bpmnTaskSetting:NotificationBpmnTaskSetting;// Workflow task configuration. Effective when type is openbpmntask
	automaticSetting:NotificationAutomaticSetting;// Automation configuration. Effective when type is openbpmntask
}
```
### NotificationReocrdSetting
Data Table Record Configuration
```ts
interface NotificationReocrdSetting {
	recordId:string;// Record ID
	moduleId:string;// Module ID
}
```
### NotificationUrlSetting
URL Configuration
```ts
interface NotificationUrlSetting {
	url:string;// URL
	isAppURL:boolean;// Whether it is an in-app URL
}
```
## Query Conditions

### AggregationQuery
Aggregation Query
```ts
interface AggregationQuery {
	func:string;// Aggregation function
	fieldId:string;// Aggregation field
	distinct:boolean;// Whether to deduplicate
}
```
### Condition
Query Condition
```ts
interface Condition {
	fieldId:string;// Field ID
	opt:string;// Operator type description: Basic comparison: eq=equals (exact match, not for list fields), ne=not equals (exclude value, not for list fields), gt=greater than (number/date), ge=greater than or equal (number/date), lt=less than (number/date), le=less than or equal (number/date); String/set matching: contains=contains substring (fuzzy search; list contains), notcontains=does not contain substring (exclude keyword, list not contains), startswith=starts with specified string (prefix match), endswith=ends with specified string (suffix match); Null check: isnull=field is null (missing data), isnotnull=field is not null (valid data); Set operations: in=value in set (multi-select match), notin=value not in set (exclude multi-select); Range check: between=value in range (range query), notbetween=value outside range (range exclusion); Tree structure: parentrooteq=root node match (direct root node), parenteq=parent node match (specified parent), parentcontains=parent node path contains (tree path), intree=in subtree (all child nodes)
	value:object;// Comparison value
	func:string;// Function: dayofyear=day of year, dayofmonth=day of month, week=day of week, weekofyear=week of year, month=month, quarter=quarter, year=year, daytonow=days to today, weektonow=weeks to today, yeartonow=years to today, monthtonow=months to today, quartertonow=quarters to today, fmtday=year-month-day format: 2021-01-01, fmtweek=year-week format: 2021-1, fmtmonth=year-month format: 2021-01, fmtquarter=year-quarter format: 2021-1, nlevel=child object level
	var:boolean;// Whether it is an expression
	formula:boolean;// Whether it is a function
	ignoreNull:boolean;// Whether to ignore null values
}
```
### Filter
Filter
```ts
interface Filter {
	opt:string;// Operator
	conditionList:array<Condition>;// Filter conditions
	children:array<Filter>;// Child filter conditions
}
```
### OrderBy
Sort Order
```ts
interface OrderBy {
	field:string;// Field name
	type:string;// Sort type
}
```
### Query
Query Condition
```ts
interface Query {
	filter:Filter;// Filter
	pageIndex:number;// Page number, default: 1
	pageSize:number;// Page size, default: 50
	orderByList:array<OrderBy>;// Sort order
	includeFields:LinkedHashSet;// Return field list
	excludeFields:Set;// Exclude field list
}
```
## SFTP

### SftpFile
SFTP File
```ts
interface SftpFile {
	filename:string;// File name
	longname:string;// Long name
	attrs:SftpFileAttr;// File attribute list
}
```
## Shared Storage

### ConvertFormatResult
Format Conversion Result
```ts
interface ConvertFormatResult {
	endConvert:boolean;// Whether conversion is complete
	error:number;// Error type
	fileTyp:string;// Converted file extension
	fileUrl:string;// File URL
	percent:number;// Conversion percentage
}
```
### ConvertFormatSetting
Format Conversion Configuration
```ts
interface ConvertFormatSetting {
	fileType:string;// Defines the type of document file to convert (required)
	outputtype:string;// Defines the resulting converted document type (required)
	password:string;// Defines the password for the file if password-protected (optional)
	region:string;// Defines the default display format for currency, date and time when converting from spreadsheet to pdf (optional)
	spreadsheetLayout:SpreadsheetLayout;// Defines settings for converting spreadsheet to pdf (optional)
	thumbnail:Thumbnail;// Defines thumbnail settings when specifying image format (bmp, gif, jpg, png) as outputtype
	title:string;// Defines the converted file name
}
```
### SpreadsheetLayout
Spreadsheet Layout
```ts
interface SpreadsheetLayout {
	fitToHeight:number;// Sets the height of the conversion area in number of pages. Default is 0.
	fitToWidth:number;// Sets the width of the conversion area in number of pages. Default is 0.
	gridLines:boolean;// Allows including or excluding grid lines in the output PDF file. Default is false.
	headings:boolean;// Allows including or excluding headings in the output PDF file. Default is false.
	ignorePrintArea:boolean;// Determines whether to ignore the print area selected for the spreadsheet file. Default is true.
	margins:SpreadsheetLayoutMargins;// Sets the margins of the output PDF file.
	orientation:string;// Sets the orientation of the output PDF file. Possible values: landscape, portrait. Default is portrait.
	pageSize:SpreadsheetLayoutPageSize;// Sets the dimensions of the output PDF file.
	scale:number;// Allows setting the scale of the output PDF file. Default is 100.
}
```
### SpreadsheetLayoutMargins
Spreadsheet Margins
```ts
interface SpreadsheetLayoutMargins {
	bottom:string;// Sets the bottom margin of the output PDF file. Default is 19.1mm.
	left:string;// Sets the left margin of the output PDF file. Default is 17.8mm.
	right:string;// Sets the right margin of the output PDF file. Default is 17.8mm.
	top:string;// Sets the top margin of the output PDF file. Default is 19.1mm.
}
```
### SpreadsheetLayoutPageSize
Spreadsheet Page Size
```ts
interface SpreadsheetLayoutPageSize {
	height:string;// Sets the page height of the output PDF file. Default is 297mm.
	width:string;// Sets the page width of the output PDF file. Default is 210mm.
}
```
### Thumbnail
Thumbnail
```ts
interface Thumbnail {
	aspect:number;// Defines the mode to fit the image to the specified height and width.
	first:boolean;// Defines whether to generate thumbnails for only the first page or for all document pages. Default is true.
	height:number;// Defines the thumbnail height in pixels. Default is 100.
	width:number;// Defines the thumbnail width in pixels. Default is 100.
}
```
## Survey

### SurveyField
Survey Field
```ts
interface SurveyField {
	id:string;// Field ID
	icon:string;// Field icon
	group:string;// Field group
	type:string;// Field type
	name:string;// Field name
	setting:Map;// Field configuration
}
```
### SurveyItem
Survey
```ts
interface SurveyItem {
	applicationId:string;// Application ID
	moduleId:string;// Module ID
	id:string;// Survey ID
	tableId:string;// Survey table ID
	name:string;// Survey name
	remark:string;// Remark
	startTime:Date;// Start time
	endTime:Date;// End time
	submitCount:number;// Submission count
	lastSubmitTime:Date;// Last submission time
	createAccountId:string;// Creator account ID
	updateAccountId:string;// Updater account ID
	sourceId:string;// Source ID
	createTime:Date;// Creation time
	updateTime:Date;// Update time
	uuid:string;// UUID
	isEnable:boolean;// Whether enabled
	rowNumber:number;// Sort order
	fieldList:array<SurveyItemField>;// Survey fields
	createAccountAvatar:string;// Creator avatar
	createAccountName:string;// Creator name
	defineId:string;// Survey definition ID
}
```
### SurveyItemDefine
Survey Definition
```ts
interface SurveyItemDefine {
	id:string;// ID
	key:string;// Identifier
	scope:string;// Scope
	name:string;// Name
	remark:string;// Remark
	createTime:string;// Creation time
	tableId:string;// Data table ID
	fieldList:array<SurveyField>;// Field list
	submitEdit:boolean;// Whether editable after submission
	allowResubmit:boolean;// Whether resubmission is allowed
	openIdFieldId:string;// Field for storing WeChat openId
	finishText:string;// Message displayed after submission
	authType:string;// Authentication method
	hideSupport:boolean;// Hide support
}
```
### SurveyItemField
Survey Field Default Value
```ts
interface SurveyItemField {
	id:string;// Field ID
	value:object;// Default value
}
```
## System

### CompanySecurityApply
Strict Authorization Application Record
```ts
interface CompanySecurityApply {
	id:string;//
	companyId:string;//
	title:string;//
	content:array<ApplyContentForm>;//
	applyAccountId:string;//
	applyAccountName:string;//
	applyAccountAvatar:string;//
	approveAccountId:string;//
	approveAccountName:string;//
	applyAccountUserName:string;//
	approveAccountAvatar:string;//
	applyTime:Date;//
	approveTime:Date;//
	status:string;// Status
	approveReason:string;//
	updateAccountId:string;//
	updateTime:Date;//
	ip:string;//
	approveIp:string;//
}
```
### LoginForm
Login Form
```ts
interface LoginForm {
	userName:string;// Username
	password:string;// Password
	type:string;// Login type
	ip:string;// IP
}
```
### LoginResult
Login Result
```ts
interface LoginResult {
	errorCode:number;// Error code
	errorMessage:string;// Error message
	token:string;// Token
	accountId:string;// Account ID
	companyId:string;// Team ID
	defaultApplicationId:string;// Default application ID
}
```
### ProcessRunArgs
Run Arguments
```ts
interface ProcessRunArgs {
	cmds:String[];// Commands
	timeout:number;// Timeout in milliseconds, 0 means no timeout
}
```
### ProcessRunResult
Run Result
```ts
interface ProcessRunResult {
	exitValue:number;// Exit code
	out:string;// Standard output
	err:string;// Error output
}
```
### RunNodeJSArgs
NodeJS Run Arguments
```ts
interface RunNodeJSArgs {
	script:string;// Script file to execute, e.g.: test/helloworld.js
	cmdline:array<String>;// Operating system has command line argument length limits, max 131071 on Linux. For large data transfers, use stdin
	stdin:string;// Standard input
	env:Map;// Environment variables
}
```
### RunWithContext
Run Context
```ts
interface RunWithContext {
	companyId:string;// Team ID
	appDefineId:string;// Application identifier
}
```
## Data Table

### DataAutomaticVar
Automation Parameter
```ts
interface DataAutomaticVar {
	value:string;// Parameter value
}
```
### DefaultValue
Data Table Default Value
```ts
interface DefaultValue {
	fieldId:string;// Field ID
	value:string;// Expression
}
```
### DeleteRecordConfig
Delete Record Configuration
```ts
interface DeleteRecordConfig {
	disableCalculateRollupField:boolean;// Whether to skip calculating lookup rollup fields, default false means calculate rollup fields
}
```
### InsertRecordConfig
Insert Record Configuration
```ts
interface InsertRecordConfig {
	disableCalculateRollupField:boolean;// Whether to skip calculating lookup rollup fields, default false means calculate rollup fields
}
```
### Table
Data Table
```ts
interface Table {
	id:string;// ID
	name:string;// Name
	key:string;// Identifier
}
```
### TableAccountSimple
Account
```ts
interface TableAccountSimple {
	id:string;// ID
	name:string;// Name
	avatar:string;// Avatar
}
```
### TableAttachment
Attachment
```ts
interface TableAttachment {
	name:string;// Name
	size:number;// Size
	id:string;// ID
	thumbnail:string;// Thumbnail
	path:string;// Path
	md5:string;// MD5 value
}
```
### TableChangeLog
Change Log
```ts
interface TableChangeLog {
	id:string;// ID
	recordId:string;// Record ID
	fieldId:string;// Field ID
	fieldName:string;// Field name
	beforeValue:string;// Value before change
	afterValue:string;// Value after change
	createTime:Date;// Creation time
	createUserId:string;// Creator ID
	createUserName:string;// Creator name
}
```
### TableComment
Comment
```ts
interface TableComment {
	comment:string;// Content
	createTime:Date;// Creation time
	createUserAvatar:string;// Creator avatar
	createUserId:string;// Creator user ID
	createUserName:string;// Creator user name
	id:number;// ID
	isDelete:boolean;// Whether deleted
	parentId:number;// Parent comment ID
	recordId:string;// Record ID
}
```
### TableCommentForm
Comment Form
```ts
interface TableCommentForm {
	recordId:string;// Record ID
	parentId:number;// Parent comment ID
	content:string;// Content
	createUserId:string;// Creator account ID
}
```
### TableCommentItem
Comment
```ts
interface TableCommentItem {
	type:string;// Type
	text:string;// Comment value
	content:array<TableCommentItem>;// Child comments
}
```
### TableField
Data Table Field
```ts
interface TableField {
	id:string;// ID
	name:string;// Field name
	key:string;// Identifier
	type:string;// Field type
	group:string;// Group
}
```
### TableFieldGroup
Data Table Field Group
```ts
interface TableFieldGroup {
	id:string;// ID
	name:string;// Group name
	key:string;// Identifier
	color:string;// Color
	showInTab:boolean;// Display group as tabs
	createAsStep:boolean;// Display as steps in creation form
}
```
### TableFieldInfo
Data Table Field Information
```ts
interface TableFieldInfo {
	id:string;// ID
	name:string;// Field name
	key:string;// Identifier
	type:string;// Field type
	icon:string;// Icon
	group:string;// Group
	displayWidth:number;// Display width
	readonly:boolean;// Whether read-only
	editableExpression:string;// Editable condition expression
	hidden:boolean;// Whether hidden
	visibleExpression:string;// Visible condition expression
	attachmentSetting:AttachmentSetting;// Attachment configuration
	treeSetting:TreeSetting;// Tree select configuration
	cascaderSetting:CascaderSetting;// Cascader select configuration
	checkboxSetting:CheckboxSetting;// Checkbox configuration
	childrenSetting:ChildrenSetting;// Children object configuration
	colorSetting:ColorSetting;// Color configuration
	coordinateSetting:CoordinateSetting;// Geolocation coordinate configuration
	createTimeSetting:CreateTimeSetting;// Creation time configuration
	createUserSetting:CreateUserSetting;// Creator configuration
	customSetting:CustomSetting;// Custom component configuration
	dateSetting:DateSetting;// Date configuration
	departmentSetting:DepartmentSetting;// Department select configuration
	doubleSetting:DoubleSetting;// Decimal
	formulaSetting:FormulaSetting;// Formula
	iDSetting:IDSetting;// ID number
	indexNumberSetting:IndexNumberSetting;// Child object number
	integerSetting:IntegerSetting;// Integer configuration
	lastModifyTimeSetting:LastModifyTimeSetting;// Last modify time configuration
	lastModifyUserSetting:LastModifyUserSetting;// Last modify user configuration
	memberSetting:UserSetting;// Member configuration
	multiTextSetting:MultiTextSetting;// Multi-line text configuration
	rateSetting:RateSetting;// Rating
	relationRecordFieldSetting:RelationRecordFieldSetting;// Relation record field configuration
	lookupListSetting:LookupListSetting;// Lookup list configuration
	lookupRollupSetting:LookupRollupSetting;// Lookup rollup configuration
	relationRecordSetting:RelationRecordSetting;// Relation record configuration
	relationRollupSetting:RelationRollupSetting;// Relation rollup configuration
	relationSetting:RelationSetting;// Relation list configuration
	richTextSetting:RichTextSetting;// Rich text configuration
	signatureSetting:SignatureSetting;// Signature configuration
	listSelectSetting:ListSelectSetting;// List select configuration
	singleTextSetting:SingleTextSetting;// Single-line text configuration
	staticTextSetting:StaticTextSetting;// Static text configuration
	timeSetting:TimeSetting;// Time configuration
	userSetting:UserSetting;// User configuration
	uUIDSetting:UUIDSetting;// UUID configuration
	seqSetting:SeqSetting;// Sequence number configuration
	validateRuleList:array<ValidateRule>;// Validation rules
	defaultValueExpression:string;// Dynamic value on creation
	defaultValueRuleList:array<DefaultValueRule>;// Default value dynamic rules, used when field changes
	appId:string;// Application ID
	tableId:string;// Data table ID
	targetAppId:string;// Target application ID, only has value for relation record fields
	requiredExpression:string;// Required condition expression
	enableChangeLog:boolean;// Whether to enable change log
	changeLogAccessRoleList:array<String>;// Change log accessible role list
	disableTooltipExpression:string;// Field tooltip when non-editable in form
}
```
### TableInfo
Data Table Information
```ts
interface TableInfo {
	id:string;// ID
	table:Table;// Data table
	tableFieldList:array<TableField>;// Data table field list
	tableFieldGroupList:array<TableFieldGroup>;// Data table field group list
}
```
### TableQuerySetting
Data Table Query Configuration
```ts
interface TableQuerySetting {
	forUpdate:boolean;// Whether to lock rows
	returnOptionName:boolean;// If there are `List Select`, `Cascader Select`, or `Tree Select` fields, also returns the option value name
	includeFields:LinkedHashSet;// Include fields to return
}
```
### TableRecordQuery
Data Table Query Condition
```ts
interface TableRecordQuery {
	filter:Filter;// Filter condition
	pageIndex:number;// Page number
	pageSize:number;// Page size
	orderByList:array<OrderBy>;// Sort order
	groupByList:array<String>;// Group by query
	returnOptionName:boolean;// Return optionName
	aggregationQueryList:array<AggregationQuery>;// Aggregation query
	includeFields:LinkedHashSet;// Return field list
	excludeFields:Set;// Exclude field list
}
```
### TableSearchSetting
Data Table Search Configuration
```ts
interface TableSearchSetting {
	searchChildrenFieldId:string;// Search children object ID
	searchTableIndex:boolean;// Show index number
	searchTableBorderStyle:string;// Table border style
	searchTableStripe:boolean;// Show stripes
	searchTableHideHeader:boolean;// Hide header
	searchChildrenFullPath:boolean;// Show children full path
	searchChildrenDefaultLevel:number;// Children default level is 1
	searchColumnList:array<TableColumnSetting>;// Searchable field list
	searchFilterId:string;// In-form selectable data filter
	searchFilterConditionList:array<ConditionSetting>;// Filter conditions
	searchOrderByList:array<OrderBy>;// Sort order
	searchTableCellStyleList:array<TableViewSettingCellStyle>;// Cell styles
	searchTableSelectionDisableExpression:string;// Row record hide expression
	filterSearchFilterId:string;// Filter condition selectable data filter
	searchFilterVarList:array<SearchFilterVar>;// Filter conditions
}
```
### TableSignature
Handwritten Signature
```ts
interface TableSignature {
	id:string;// ID
	accountId:string;// Account ID
	accountName:string;// Account name
	uploadTime:Date;// Upload time
	path:string;// Path
}
```
### TableValidateFormResult
Data Table Form Validation Result
```ts
interface TableValidateFormResult {
	itemList:array<TableValidateFormItem>;//
}
```
### UpdateRecordConfig
Update Record Configuration
```ts
interface UpdateRecordConfig {
	enableChangeLog:boolean;// Whether to enable change log, default false
	disableCalculateRollupField:boolean;// Whether to skip calculating lookup rollup fields, default false means calculate rollup fields
	updateBpmnInstaceFormVar:boolean;// Whether to sync update workflow instance form variables, default false
}
```
### SearchFilterVar
Filter Condition
```ts
interface SearchFilterVar {
	id:string;// ID
	valueExpression:string;// Condition expression
}
```
## Search Engine

### TextindexDocument
Document Object
```ts
interface TextindexDocument {
	applicationId:string;// Application ID
	tableId:string;//
	tableName:string;//
	recordId:string;// Record ID
	title:string;// Title
	content:string;// Content
	openAutomaticId:string;// Open automation ID
	contentHighlight:array<String>;// Highlighted parts
	fieldValueList:array<TextindexDocumentField>;//
}
```
### TextindexDocumentField
Document Field Object
```ts
interface TextindexDocumentField {
	fieldId:string;// Field ID
	fieldName:string;// Field name
	fieldType:string;// Field type
	value:object;// Original value
	stringValue:string;// Display value
	isTitle:boolean;// Whether it is a title
	isAttr:boolean;// Whether it is an attribute
}
```
### TextindexSearchQuery
Search Engine Query Object
```ts
interface TextindexSearchQuery {
	keyword:string;// Keyword
	tableIdList:array<String>;// Data source identifier list
	pageIndex:number;// Page number, starting from 1
	pageSize:number;// Page size
}
```
### TextindexSearchResult
Search Engine Search Result
```ts
interface TextindexSearchResult {
	count:number;// Total count
	list:array<TextindexDocument>;// Document list
}
```
## User

### User
User
```ts
interface User {
	id:string;// ID
	name:string;// Name
	avatar:string;// Avatar
	roleList:array<String>;// Roles
	departmentList:array<String>;// Departments
	leaderList:array<String>;// Direct supervisors
	companyRoleList:array<String>;// Team role list
	weworkUserId:string;// WeCom account ID
	dingtalkUserId:string;// DingTalk account ID
	feishuUserId:string;// Feishu account ID
	userInfo:object;// Automation extended information
	permissionList:Set;// Permission list
}
```
### UserInfo
User Information
```ts
interface UserInfo {
	userName:string;// Username
	mobileNo:string;// Mobile number
	email:string;// Email
	oid:string;// OID
	remark:string;// Remark
	id:string;// ID
	name:string;// Name
	avatar:string;// Avatar
	roleList:array<String>;// Roles
	departmentList:array<String>;// Departments
	leaderList:array<String>;// Direct supervisors
	companyRoleList:array<String>;// Team role list
	weworkUserId:string;// WeCom account ID
	dingtalkUserId:string;// DingTalk account ID
	feishuUserId:string;// Feishu account ID
	userInfo:object;// Automation extended information
	permissionList:Set;// Permission list
}
```
### UserRole
Application Role
```ts
interface UserRole {
	id:string;// ID
	name:string;// Name
	isAdmin:boolean;// Whether administrator
	permissionList:array<String>;// Permission list
	remark:string;// Remark
}
```
## Website

### WebsiteResource
Website Resource
```ts
interface WebsiteResource {
	id:string;// ID
	name:string;// Name
	path:string;// Path
	isDirectory:boolean;// Whether directory
	fileId:string;// File ID
}
```
## Word

### WordPicture
Word Picture
```ts
interface WordPicture {
	url:string;// URL
	path:string;// Path
	storagePath:string;// Storage path
	width:number;// Width
	height:number;// Height
}
```
