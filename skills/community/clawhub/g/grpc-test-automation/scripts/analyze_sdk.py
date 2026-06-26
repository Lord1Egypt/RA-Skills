#!/usr/bin/env python3
"""
SDK Analyzer - Analyze C/C++ SDK headers and extract interface definitions
"""

import re
import sys
import os
import json
from pathlib import Path


class SDKAnalyzer:
    """Analyze SDK header files"""
    
    def __init__(self, sdk_include_dir):
        self.sdk_dir = Path(sdk_include_dir)
        self.functions = []
        self.enums = []
        self.structs = []
        self.error_codes = []
        
    def analyze(self):
        """Analyze all header files"""
        for header_file in self.sdk_dir.glob("*.h"):
            print(f"Analyzing: {header_file.name}")
            self._parse_header(header_file)
        
        return {
            'functions': self.functions,
            'enums': self.enums,
            'structs': self.structs,
            'error_codes': self.error_codes
        }
    
    def _parse_header(self, header_file):
        """Parse a single header file"""
        with open(header_file, 'r') as f:
            content = f.read()
        
        # Remove comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = re.sub(r'//.*', '', content)
        
        # Extract enums
        self._extract_enums(content)
        
        # Extract structs
        self._extract_structs(content)
        
        # Extract functions
        self._extract_functions(content)
    
    def _extract_enums(self, content):
        """Extract enum definitions"""
        # Pattern: typedef enum { ... } name_t;
        pattern = r'typedef\s+enum\s*\{([^}]+)\}\s*(\w+)_t\s*;'
        
        for match in re.finditer(pattern, content):
            body = match.group(1)
            type_name = match.group(2)
            
            # Extract enum values
            values = []
            for line in body.split(','):
                line = line.strip()
                if '=' in line:
                    name, value = line.split('=')
                    values.append({
                        'name': name.strip(),
                        'value': int(value.strip())
                    })
                elif line and not line.startswith('//'):
                    values.append({'name': line.strip()})
            
            enum_def = {
                'type_name': type_name,
                'proto_name': self._to_proto_enum_name(type_name),
                'values': values
            }
            
            self.enums.append(enum_def)
            
            # Check if it's an error code enum
            if 'error' in type_name.lower() or 'err' in type_name.lower():
                self.error_codes.extend(values)
    
    def _extract_structs(self, content):
        """Extract struct definitions"""
        # Pattern: typedef struct { ... } name_t;
        pattern = r'typedef\s+struct\s*\{([^}]+)\}\s*(\w+)_t\s*;'
        
        for match in re.finditer(pattern, content):
            body = match.group(1)
            type_name = match.group(2)
            
            # Extract fields
            fields = []
            for line in body.split(';'):
                line = line.strip()
                if not line or line.startswith('//'):
                    continue
                
                # Parse field: type name or type name[N]
                field_match = re.match(r'(\w+[\s\*]+)\s*(\w+)(?:\[(\d+)\])?', line)
                if field_match:
                    c_type = field_match.group(1).strip()
                    field_name = field_match.group(2)
                    array_size = field_match.group(3)
                    
                    proto_type = self._c_type_to_proto(c_type, array_size)
                    
                    fields.append({
                        'c_type': c_type,
                        'c_name': field_name,
                        'proto_type': proto_type,
                        'proto_name': field_name,
                        'is_array': bool(array_size)
                    })
            
            self.structs.append({
                'type_name': type_name,
                'proto_name': self._to_proto_message_name(type_name),
                'fields': fields
            })
    
    def _extract_functions(self, content):
        """Extract function declarations"""
        # Pattern: return_type func_name(params);
        # Looks for lines ending with ;
        for line in content.split('\n'):
            line = line.strip()
            if not line.endswith(';'):
                continue
            
            # Match function pattern
            func_match = re.match(r'(\w+)\s+(\w+)\s*\(([^)]*)\)\s*;', line)
            if func_match:
                return_type = func_match.group(1)
                func_name = func_match.group(2)
                params = func_match.group(3)
                
                # Skip if looks like a variable declaration
                if return_type in ['int', 'char', 'void'] and not func_name.startswith('venc_'):
                    continue
                
                # Parse parameters
                param_list = self._parse_params(params)
                
                # Generate proto method name
                proto_name = self._to_proto_method_name(func_name)
                
                self.functions.append({
                    'c_name': func_name,
                    'proto_name': proto_name,
                    'return_type': return_type,
                    'params': param_list
                })
    
    def _parse_params(self, params_str):
        """Parse function parameters"""
        params = []
        if not params_str.strip() or params_str.strip() == 'void':
            return params
        
        for param in params_str.split(','):
            param = param.strip()
            if not param:
                continue
            
            # Parse: [const] type [*] name
            param_match = re.match(r'(?:const\s+)?(\w+)\s*(\*?)\s*(\w+)', param)
            if param_match:
                c_type = param_match.group(1)
                is_pointer = param_match.group(2) == '*'
                name = param_match.group(3)
                
                params.append({
                    'c_type': c_type,
                    'c_name': name,
                    'is_pointer': is_pointer,
                    'is_output': is_pointer and 'error' not in c_type.lower()
                })
        
        return params
    
    def _c_type_to_proto(self, c_type, array_size=None):
        """Convert C type to proto type"""
        type_map = {
            'char': 'string' if array_size else 'int32',
            'uint8_t': 'uint32',
            'int8_t': 'int32',
            'uint16_t': 'uint32',
            'int16_t': 'int32',
            'uint32_t': 'uint32',
            'int32_t': 'int32',
            'uint64_t': 'uint64',
            'int64_t': 'int64',
            'float': 'float',
            'double': 'double',
            'bool': 'bool',
        }
        
        if c_type in type_map:
            return type_map[c_type]
        
        # Check if it's an enum or struct type
        for enum in self.enums:
            if c_type == f"{enum['type_name']}_t":
                return enum['proto_name']
        
        for struct in self.structs:
            if c_type == f"{struct['type_name']}_t":
                return struct['proto_name']
        
        return 'string'  # Default
    
    def _to_proto_enum_name(self, c_name):
        """Convert C enum name to proto enum name"""
        # Remove common prefixes/suffixes
        name = c_name.upper()
        name = re.sub(r'^VENC_', '', name)
        name = re.sub(r'_T$', '', name)
        return name
    
    def _to_proto_message_name(self, c_name):
        """Convert C struct name to proto message name"""
        # Convert to PascalCase
        name = c_name.lower()
        name = re.sub(r'^venc_', '', name)
        return ''.join(word.capitalize() for word in name.split('_'))
    
    def _to_proto_method_name(self, func_name):
        """Convert C function name to proto method name"""
        # Remove prefix
        name = re.sub(r'^venc_', '', func_name)
        # Convert to PascalCase
        return ''.join(word.capitalize() for word in name.split('_'))


def generate_proto(analyzer_result, package_name='service'):
    """Generate proto file from analysis result"""
    lines = []
    lines.append('syntax = "proto3";')
    lines.append('')
    lines.append(f'package {package_name};')
    lines.append('')
    
    # Enums
    for enum in analyzer_result['enums']:
        lines.append(f'enum {enum["proto_name"]} {{')
        for value in enum['values']:
            if 'value' in value:
                lines.append(f'    {value["name"]} = {value["value"]};')
            else:
                lines.append(f'    {value["name"]};')
        lines.append('}')
        lines.append('')
    
    # Messages
    for struct in analyzer_result['structs']:
        lines.append(f'message {struct["proto_name"]} {{')
        for i, field in enumerate(struct['fields'], 1):
            repeated = 'repeated ' if field['is_array'] else ''
            lines.append(f'    {repeated}{field["proto_type"]} {field["proto_name"]} = {i};')
        lines.append('}')
        lines.append('')
    
    # Service
    lines.append(f'service {package_name.capitalize()}Service {{')
    for func in analyzer_result['functions']:
        req_name = f'{func["proto_name"]}Request'
        resp_name = f'{func["proto_name"]}Response'
        lines.append(f'    rpc {func["proto_name"]} ({req_name}) returns ({resp_name});')
    lines.append('}')
    lines.append('')
    
    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_sdk.py <sdk_include_dir> [output.proto]")
        sys.exit(1)
    
    sdk_dir = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'service.proto'
    
    analyzer = SDKAnalyzer(sdk_dir)
    result = analyzer.analyze()
    
    print(f"\nFound:")
    print(f"  - {len(result['functions'])} functions")
    print(f"  - {len(result['enums'])} enums")
    print(f"  - {len(result['structs'])} structs")
    
    # Generate proto
    proto_content = generate_proto(result)
    
    with open(output_file, 'w') as f:
        f.write(proto_content)
    
    print(f"\nProto file generated: {output_file}")
    
    # Also save analysis as JSON
    json_file = output_file.replace('.proto', '_analysis.json')
    with open(json_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Analysis saved: {json_file}")


if __name__ == '__main__':
    main()
