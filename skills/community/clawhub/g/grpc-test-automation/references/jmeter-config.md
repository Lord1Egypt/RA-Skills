# JMeter gRPC Plugin Configuration

## Prerequisites

1. Apache JMeter 5.6+
2. jmeter-grpc-request plugin (jmeter-grpc-request-1.1.1.jar)
3. Proto descriptor file (.protobin)

## Plugin Installation

```bash
# Copy plugin to JMeter
cp jmeter-grpc-request-1.1.1.jar /opt/jmeter/lib/ext/

# Verify installation
ls /opt/jmeter/lib/ext/jmeter-grpc-request*.jar
```

## Proto Descriptor Generation

The proto descriptor is required by JMeter to understand gRPC service definitions.

```bash
# Generate from proto file
protoc --descriptor_set_out=service.protobin \
       --include_imports \
       -I ./proto \
       ./proto/service.proto

# Or using Python grpc_tools
python3 -m grpc_tools.protoc \
    -Iproto \
    --descriptor_set_out=service.protobin \
    --include_imports \
    proto/service.proto
```

## JMX Configuration

### GRPCSampler Structure

```xml
<vn.zalopay.benchmark.GRPCSampler 
    guiclass="vn.zalopay.benchmark.GRPCSamplerGui" 
    testclass="vn.zalopay.benchmark.GRPCSampler" 
    testname="Test Name" enabled="true">
  
  <!-- Proto descriptor path (absolute path) -->
  <stringProp name="GRPCSampler.proto">/path/to/service.protobin</stringProp>
  
  <!-- Proto folder (for imports) -->
  <stringProp name="GRPCSampler.protoFolder">/path/to/proto</stringProp>
  
  <!-- Server connection -->
  <stringProp name="GRPCSampler.host">${SERVER_HOST}</stringProp>
  <stringProp name="GRPCSampler.port">${SERVER_PORT}</stringProp>
  
  <!-- gRPC method (full path) -->
  <stringProp name="GRPCSampler.fullMethod">package.ServiceName/MethodName</stringProp>
  
  <!-- Request JSON -->
  <stringProp name="GRPCSampler.requestJson">{&quot;field&quot;: &quot;value&quot;}</stringProp>
  
  <!-- TLS (false for plaintext) -->
  <boolProp name="GRPCSampler.tls">false</boolProp>
  
  <!-- Optional: Metadata -->
  <stringProp name="GRPCSampler.metadata"></stringProp>
  
  <!-- Optional: Deadline (ms, 0 = no timeout) -->
  <stringProp name="GRPCSampler.deadline">0</stringProp>
  
</vn.zalopay.benchmark.GRPCSampler>
```

### Field Descriptions

| Field | Description | Example |
|-------|-------------|---------|
| `proto` | Absolute path to .protobin file | `/home/user/grpc_test/jmeter/service.protobin` |
| `protoFolder` | Directory containing proto files | `/home/user/grpc_test/proto` |
| `host` | Server hostname or IP | `localhost` or `192.168.1.100` |
| `port` | Server port | `8080` |
| `fullMethod` | Full gRPC method path | `venc.VencService/GetDeviceInfo` |
| `requestJson` | JSON request body | `{"device_id": "BOARD-001"}` |
| `tls` | Enable TLS | `false` for plaintext |
| `metadata` | gRPC metadata (key:value) | `authorization:Bearer token` |
| `deadline` | Request timeout in ms | `5000` |

### Request JSON Format

Use protobuf JSON mapping:

| Proto Type | JSON Example |
|------------|--------------|
| string | `"field": "value"` |
| int32/uint32 | `"field": 123` |
| int64/uint64 | `"field": "123456789"` (as string or number) |
| bool | `"field": true` |
| enum | `"field": 0` (numeric value) |
| message | `"field": {"nested": "value"}` |
| repeated | `"field": [1, 2, 3]` |

## Variable Extraction

### Regex Extractor (Recommended)

Extract session_id from response:

```xml
<RegexExtractor guiclass="RegexExtractorGui" 
    testclass="RegexExtractor" 
    testname="Extract SessionID" enabled="true">
  <stringProp name="RegexExtractor.useHeaders">false</stringProp>
  <stringProp name="RegexExtractor.refname">SESSION_ID</stringProp>
  <stringProp name="RegexExtractor.regex">&quot;sessionId&quot;:\s*(\d+)</stringProp>
  <stringProp name="RegexExtractor.template">$1$</stringProp>
  <stringProp name="RegexExtractor.default"></stringProp>
  <stringProp name="RegexExtractor.match_number">1</stringProp>
</RegexExtractor>
```

### Important: Extractor Placement

The extractor MUST be a **child** of the sampler that generates the value:

```xml
<!-- Correct -->
<GRPCSampler testname="StartEncoding">
  <hashTree>
    <RegexExtractor testname="Extract ID">  <!-- Child node -->
      ...
    </RegexExtractor>
  </hashTree>
</GRPCSampler>
<hashTree/>

<GRPCSampler testname="StopEncoding">
  <!-- Can use ${SESSION_ID} here -->
</GRPCSampler>

<!-- Wrong -->
<GRPCSampler testname="StartEncoding"/>
<RegexExtractor testname="Extract ID"/>  <!-- Sibling - won't work! -->
<GRPCSampler testname="StopEncoding"/>
```

## Using Extracted Variables

```xml
<!-- Reference variable with ${VAR_NAME} -->
<stringProp name="GRPCSampler.requestJson">
  {&quot;sessionId&quot;: ${SESSION_ID}}
</stringProp>
```

## Thread Group Configuration

```xml
<ThreadGroup guiclass="ThreadGroupGui" 
    testclass="ThreadGroup" 
    testname="Test Group" enabled="true">
  <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
  <elementProp name="ThreadGroup.main_controller" elementType="LoopController">
    <boolProp name="LoopController.continue_forever">false</boolProp>
    <stringProp name="LoopController.loops">1</stringProp>
  </elementProp>
  <stringProp name="ThreadGroup.num_threads">1</stringProp>
  <stringProp name="ThreadGroup.ramp_time">1</stringProp>
</ThreadGroup>
```

## Common Issues

### Issue: "Protoc invocation failed"

**Cause:** Plugin cannot parse proto file

**Solution:** 
- Use absolute path for proto file
- Ensure .protobin file is valid
- Check proto syntax

### Issue: Variable not substituted

**Cause:** Extractor not executed or wrong placement

**Solution:**
- Place extractor as child of sampler
- Check regex matches actual response
- Verify variable name matches

### Issue: "Unable to read messages"

**Cause:** Invalid JSON in request

**Solution:**
- Escape quotes properly: `&quot;`
- Use correct field names (camelCase for protobuf JSON)
- Check JSON syntax

## Running Tests

```bash
# Command line execution
/opt/jmeter/bin/jmeter -n \
    -t test.jmx \
    -l results.jtl \
    -j jmeter.log \
    -JSERVER_HOST=localhost \
    -JSERVER_PORT=8080

# Generate HTML report
/opt/jmeter/bin/jmeter -g results.jtl -o report/
```
