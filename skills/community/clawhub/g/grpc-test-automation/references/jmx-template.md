# JMX Template Guide

## JMX Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.6.3">
  <hashTree>
    <TestPlan>...</TestPlan>
    <hashTree>
      <ThreadGroup>...</ThreadGroup>
      <hashTree>
        <GRPCSampler>...</GRPCSampler>
        <hashTree/>
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
```

## GRPCSampler Template

```xml
<vn.zalopay.benchmark.GRPCSampler 
    guiclass="vn.zalopay.benchmark.GRPCSamplerGui" 
    testclass="vn.zalopay.benchmark.GRPCSampler" 
    testname="${TEST_NAME}" enabled="true">
  <stringProp name="GRPCSampler.proto">${PROTO_PATH}</stringProp>
  <stringProp name="GRPCSampler.protoFolder">${PROTO_DIR}</stringProp>
  <stringProp name="GRPCSampler.host">${SERVER_HOST}</stringProp>
  <stringProp name="GRPCSampler.port">${SERVER_PORT}</stringProp>
  <stringProp name="GRPCSampler.fullMethod">${SERVICE}/${METHOD}</stringProp>
  <stringProp name="GRPCSampler.requestJson">${REQUEST_JSON}</stringProp>
  <boolProp name="GRPCSampler.tls">false</boolProp>
</vn.zalopay.benchmark.GRPCSampler>
```

## Variable Extraction

### Regex Extractor (Recommended)
```xml
<RegexExtractor guiclass="RegexExtractorGui" 
    testclass="RegexExtractor" 
    testname="Extract SessionID" enabled="true">
  <stringProp name="RegexExtractor.refname">SESSION_ID</stringProp>
  <stringProp name="RegexExtractor.regex">&quot;sessionId&quot;:\s*(\d+)</stringProp>
  <stringProp name="RegexExtractor.template">$1$</stringProp>
  <stringProp name="RegexExtractor.default"></stringProp>
</RegexExtractor>
```

### JSON Post Processor
```xml
<JSONPostProcessor guiclass="JSONPostProcessorGui" 
    testclass="JSONPostProcessor" 
    testname="Extract SessionID" enabled="true">
  <stringProp name="JSONPostProcessor.referenceNames">SESSION_ID</stringProp>
  <stringProp name="JSONPostProcessor.jsonPathExprs">$.sessionId</stringProp>
  <stringProp name="JSONPostProcessor.match_numbers">1</stringProp>
</JSONPostProcessor>
```

## Test Plan Variables

```xml
<elementProp name="TestPlan.user_defined_variables" elementType="Arguments">
  <collectionProp name="Arguments.arguments">
    <elementProp name="SERVER_HOST" elementType="Argument">
      <stringProp name="Argument.name">SERVER_HOST</stringProp>
      <stringProp name="Argument.value">localhost</stringProp>
    </elementProp>
    <elementProp name="SERVER_PORT" elementType="Argument">
      <stringProp name="Argument.name">SERVER_PORT</stringProp>
      <stringProp name="Argument.value">8080</stringProp>
    </elementProp>
  </collectionProp>
</elementProp>
```

## Listener Configuration

```xml
<ResultCollector guiclass="ViewResultsFullVisualizer" 
    testclass="ResultCollector" 
    testname="View Results Tree" enabled="true">
  <boolProp name="ResultCollector.error_logging">false</boolProp>
</ResultCollector>
```

## Important Notes

1. **Proto path**: Use absolute path to `.proto` file
2. **ProtoFolder**: Set to directory containing proto files
3. **TLS**: Set to `false` for plaintext connections
4. **Variable scope**: Regex Extractor must be child of sampler that generates the value
