<!-- DOCKEY: api-6c1f4 -->
This document is the API documentation for the Informat low-code platform.

## Overview
The Informat API allows external systems to interact with applications via the HTTP protocol. Each API has a unique access path. When an HTTP request arrives, the configured automation program or script function is executed, and the execution result is returned to the caller in the configured format.

The API execution process includes:
(Optional) Pre-processing script
Main script function execution
(Optional) Post-processing script
(Optional) Error handling script

## ApiDefine Definition

An ApiDefine corresponds to one API endpoint. Its definition structure is as follows:

```
{
  // HTTP path (unique)
  path: String,

  // Return value type: "json" | "text" | "file" | "redirect"
  view: String,

  // Invocation type: "script"
  invokeType: String,

  // HTTP method
  method: String,

  // Script called before API invocation
  beforeScriptId: String,      // @Ref(CallScript)
  beforeScriptFunc: String,

  // Script called for API invocation
  scriptId: String,            // @Ref(CallScript)
  scriptFunc: String,

  // Script called after API invocation
  afterScriptId: String,       // @Ref(CallScript)
  afterScriptFunc: String,

  // Script called on API invocation error
  errorScriptId: String,       // @Ref(CallScript)
  errorScriptFunc: String,

  // Description
  apiDesc: String,

  // Whether enabled
  isEnable: boolean,

  // Whether to output keys with null values when view=json (default false)
  jsonConfigWriteMapNullValue: boolean,

  // Rate limiting configuration
  enableRateLimiter: boolean,  // Enable rate limiting
  rateLimiterQps: double,      // Queries per second, 0 means no limit
  rateLimiterTimeout: int,     // Timeout duration (milliseconds)
  rateLimiterKeyVar: String    // Rate limiting key expression
}

```

[Important Rules]
- All scriptId / scriptFunc referenced in ApiDefine must actually exist in the application. It is forbidden to reference scripts or functions that have not yet been created in the API definition.
- All script functions must be explicitly exported using export function

## Access Path

It is important to note that API preview access and production access differ in usage and behavior. Please distinguish between them during development and invocation.

### Preview Access

Only available before the application is published, used for development, debugging, and testing phases.

```
https://$host/web0/api/preview/${appId}/${path}
```

- ${host} Informat service address, can be obtained via `_app_get_web_url`
- ${appId} is the application ID, can be obtained via `_query_app_define_designer`
- ${path} is the configured path


### Production Access

Only available after the application is published, for real business scenarios.

```
https://$host/web0/api/${appId}/${path}
```

- ${host} Informat service address, can be obtained via `_app_get_web_url`
- ${appId} is the application ID, can be obtained via `_query_app_define_designer`
- ${path} is the configured path

### Notes
- Before the application is published, external systems cannot call the API through the production access path
- Do not use preview access URLs in production environments (the website module must use the production access path when calling APIs)


## Pre-processing

If pre-execution is configured, the pre-processing script will be executed before calling the script or automation. By setting up pre-processing, you can conveniently implement features like authentication and auditing. If the pre-processing script throws an exception, the API call will return an error. If the pre-processing script has a return value, the API will directly return this value.

The pre-processing script accepts one parameter of type APIContext.


The structure of InformatHttpRequest is as follows:

```
{
	Object getAttribute(String name);// Get the attribute with the specified name
	Enumeration<String> getAttributeNames();// Get the names of all attributes
	String getCharacterEncoding();// Get the character encoding of the current HTTP request
	String getParameter(String name);// Get the value of the request parameter with the specified name
	Enumeration<String> getParameterNames();// Get an enumeration of all parameter names in the current HTTP request
	String[] getParameterValues(String name);// Get all values of the request parameter with the specified name
	Map<String, String[]> getParameterMap();// Get all request parameter key-value pairs
	String getProtocol();// Get the protocol used by the client (e.g., HTTP/1.1)
	String getScheme();// Get the scheme used by the client (e.g., http or https)
	String getServerName();// Get the hostname of the server where the current web application resides
	String getRemoteAddr();// Get the IP address of the client that sent the request
	String getRemoteHost();// Get the hostname of the client that sent the request
	int getRemotePort();// Get the port number used by the client that sent the request
	void setAttribute(String name, Object o);// Set the attribute with the specified name to the specified value
	void removeAttribute(String name);// Remove the attribute with the specified name from this request
	boolean isSecure();// Returns true if this request was made using a secure protocol (e.g., HTTPS); otherwise returns false
	int getServerPort();// Get the port number of the server where the current web application resides
	String getContentType();// Get the content type of the HTTP request
	String getAuthType();// Return the name of the authentication scheme used for the request
	Cookie[] getCookies();// Return an array containing all cookies included in this request
	String getHeader(String name);// Get the value of the request header with the specified name
	Enumeration<String> getHeaders(String name);// Get all values of the request header with the specified name
	Enumeration<String> getHeaderNames();// Get an enumeration of all request header names in the current HTTP request
	String getMethod();// Get the HTTP method of the request, e.g., GET, POST, etc.
	String getPathInfo();// Get the path after the portion of the request URL that matches the Servlet mapping
	String getContextPath();// Return the context path of the web application associated with the request
	String getQueryString();// Get the query string portion of the request URL
	String getRemoteUser();// Get the username of the client that sent the request
	java.security.Principal getUserPrincipal();
	String getRequestURI();// Get the URI of the request
	String getServletPath();// Get the Servlet path requested by the client
	Collection<Part> getParts();// Get all Part components in an HTTP POST request
}
```

The structure of InformatHttpResponse is as follows:

```
{
	String getCharacterEncoding();// Return the character encoding of the response
	String getContentType();// Return the content type of the response
	ServletOutputStream getOutputStream();// Return a ServletOutputStream for writing bytes to the response output stream
	PrintWriter getWriter();// Get a PrintWriter object for writing characters to the response output stream
	void setCharacterEncoding(String charset);// Set the character encoding of the response content
	void setContentLength(int len);// Set the length of the response content
	void setContentLengthLong(long len);// Set the length of the response content, similar to setContentLength but supports longer content lengths
	void setContentType(String type);// Set the MIME type of the response content
	boolean containsHeader(String name);// Return whether the header with the specified name has been set
	String encodeURL(String url);// Encode the specified URL for use when sending the response
	void sendError(int sc, String msg);// Send an error code and message to the client and clear the response buffer
	void sendError(int sc);// Send an error code to the client and clear the response buffer
	void sendRedirect(String location);// Redirect to the specified URL
	void setHeader(String name, String value);// Set the value of the response header with the specified name
	void addHeader(String name, String value);// Add a header with the specified name and value to the response
	void setDateHeader(String name, long date);// Set a date header with the specified name and value, representing the response send date
	void addDateHeader(String name, long date);// Add a date header with the specified name and value, representing the response send date
	void setIntHeader(String name, int value);// Set an integer header with the specified name and value to the response
	void addIntHeader(String name, int value);// Add an integer header with the specified name and value to the response
	void setStatus(int sc);// Set the response status code
	int getStatus();// Get the response status code
	String getHeader(String name);// Return the value of the response header with the specified name
	Collection<String> getHeaders(String name);// Get all values of the response header with the specified name
	int getBufferSize();// Return the size of the response output buffer
	void setBufferSize(int size);// Set the size of the response buffer
	void flushBuffer();// Flush the response output stream
	void reset();// Clear the response buffer
	void resetBuffer();// Clear the response buffer
	boolean isCommitted();// Return whether the response has been committed
}
```

The structure of Part is as follows:

```
{
	name:String,// Name specified during upload
	contentType:String,// File type
	size:Integer,// File size
	submittedFileName:String,// Original file name
	save(path),// Save to local sandbox
	saveStorage(path),// Save to shared storage
    saveAttachment(tableId,fieldId):TableAttachment// Save the file as an attachment field
}
```

### Example

Authentication before API invocation: check whether the token is valid; if invalid, return a token expired error.

1. Configure the example API (test) with a pre-processing script and script function, e.g., preHandle

2. The pre-processing script function is as follows:

```js
export function preHandle(ctx) {
	console.log('preHandle',ctx);
	var token=ctx.query['token'];
	console.log('token',token);
	if(token==null){
		informat.app.abort('token cannot be null');
		return;
	}
	var account=informat.system.getAccountByToken(token);
	if(account==null){
		informat.app.abort('token expired');
		return;
	}
	ctx.request.setAttribute('account',account);// Subsequent scripts can get the accessing user info via ctx.request.getAttribute('account')
}
```

## APIContext Description (Very Important)

All API script functions receive a parameter ctx of type APIContext.

The structure of APIContext is as follows:

```
{
	headers:Object,// Request headers
	cookies:Object,// Request cookies
	query:Object,// Request query parameters (GET parameters)
	body:String,// POST request body
	url:String,// Full request path
	appId:String,// appId that the API belongs to
	path:String,// API path
	method:String,// HTTP request method
	getParts():Part// Uploaded files
	request:InformatHttpRequest,// HTTP request object
	response:InformatHttpResponse,// HTTP response object
}
```

[Parameter Retrieval Rules (Must Follow)]
- The params field does not exist in APIContext
- GET / URL parameters: must be retrieved via ctx.query
- POST request body: retrieved via ctx.body


## Script Function Format

When the invocation type is script, you need to export the function using the export syntax in the script file. The script function needs to accept a ctx parameter.

For example, to implement a function that returns the current time via an API, the script file is apitest.js, which contains a function getTime for getting the current time.

apitest.js

```js
export function getTime(ctx){
    return new Date()
}
```

## Return Value Types

### JSON

When the return value type is JSON, JSON-formatted text will be returned. The HTTP response content-type will be set to application/json;charset=UTF-8. The automation program or script function being called needs to return an object, and the system will automatically serialize the object to a JSON string.

### Text

When the return value type is text, plain text will be returned. The HTTP response content-type will be set to text/plain;charset=UTF-8. The automation program or script function being called can return any format. If the return value is an object, the system will call the object's toString method to convert it to a string. If the return value is null, an empty string will be returned.