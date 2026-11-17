"""Validate the server's V2 user-parameter contract without task side effects.

Only the schema contract published by action-common/skill is supported,
including the custom numeric multi-interval ``range`` keyword.
Schema definitions are validated by the server at save/publish time.
Schema defaults are annotations; execution defaults remain in invoke.params.
"""

import math


class ParameterValidationError(ValueError):
    """The supplied user parameters do not satisfy the published contract."""


class SchemaConfigurationError(RuntimeError):
    """The server supplied an unsupported or malformed parameter schema."""


def _is_number(value):
    return type(value) is int or (type(value) is float and math.isfinite(value))


def _json_equal(left, right):
    """Keep JSON booleans distinct from numbers, including in nested enums."""
    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left == right
    if isinstance(left, dict) and isinstance(right, dict):
        return left.keys() == right.keys() and all(_json_equal(left[k], right[k]) for k in left)
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all(_json_equal(a, b) for a, b in zip(left, right))
    return left == right


def _validate_value(schema, value, path):
    """Validate JSON values without type coercion, mutation or default injection."""
    if not isinstance(schema, dict):
        raise SchemaConfigurationError(path + ': 服务端 params_schema 必须是对象')
    kind = schema.get("type", "")
    matches = {
        "": True, "object": isinstance(value, dict), "array": isinstance(value, list),
        "string": isinstance(value, str), "boolean": isinstance(value, bool),
        "null": value is None, "number": _is_number(value),
        "integer": _is_number(value) and int(value) == value,
    }
    if not isinstance(kind, str) or kind not in matches:
        raise SchemaConfigurationError(path + ': 服务端 params_schema 的 type 不受支持')
    if "range" in schema:
        ranges = schema["range"]
        if (kind not in ("number", "integer") or not isinstance(ranges, list) or not ranges
                or any(not isinstance(bounds, list) or len(bounds) != 2
                       or not all(_is_number(endpoint) for endpoint in bounds)
                       or bounds[0] > bounds[1] for bounds in ranges)):
            raise SchemaConfigurationError(path + ': 服务端 params_schema 的 range 配置无效')
    if not matches[kind]:
        raise ParameterValidationError(path + ": expected " + kind)
    if "range" in schema and not any(low <= value <= high for low, high in schema["range"]):
        raise ParameterValidationError(path + ": number is outside the allowed ranges")
    if "enum" in schema and not any(_json_equal(value, item) for item in schema["enum"]):
        raise ParameterValidationError(path + ": value is not in enum")
    if "const" in schema and not _json_equal(value, schema["const"]):
        raise ParameterValidationError(path + ": value does not match const")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                raise ParameterValidationError(path + "." + key + ": required")
        properties = schema.get("properties", {})
        for key in sorted(value):
            if key in properties:
                _validate_value(properties[key], value[key], path + "." + key)
            elif schema.get("additionalProperties") is False:
                raise ParameterValidationError(path + "." + key + ": unknown parameter")
    elif isinstance(value, (str, list)):
        low, high = ("minLength", "maxLength") if isinstance(value, str) else ("minItems", "maxItems")
        if len(value) < schema.get(low, 0) or (high in schema and len(value) > schema[high]):
            raise ParameterValidationError(path + ": length out of range")
        if isinstance(value, list) and "items" in schema:
            for index, item in enumerate(value):
                _validate_value(schema["items"], item, path + "[" + str(index) + "]")
    elif _is_number(value):
        if (("minimum" in schema and value < schema["minimum"]) or
                ("maximum" in schema and value > schema["maximum"])):
            raise ParameterValidationError(path + ": number out of range")


def validate_parameters(schema, params):
    """Check merged user parameters; execution defaults are never synthesized."""
    _validate_value(schema, params, "params")


class OptionsSourceError(RuntimeError):
    """Remote options could not be obtained or violate the response contract."""


def _pointer_tokens(path):
    if not isinstance(path, str) or not path.startswith("/"):
        raise ValueError('字段必须是相对 params 根的 JSON Pointer')
    tokens = path[1:].split("/")
    for token in tokens:
        for index, char in enumerate(token):
            if char == "~" and (index + 1 == len(token) or token[index + 1] not in "01"):
                raise ValueError('JSON Pointer 转义无效')
    return [token.replace("~1", "/").replace("~0", "~") for token in tokens]


def options_field(schema, path):
    """Resolve an advertised field, including item-level choices on array fields."""
    node = schema
    for token in _pointer_tokens(path):
        if node.get("type") == "array":
            if not token.isascii() or not token.isdigit() or str(int(token)) != token:
                raise ValueError('数组字段路径无效')
            node = node.get("items", {})
        else:
            node = node.get("properties", {}).get(token, {})
    if node.get("options_source") is None and node.get("type") == "array":
        node = node.get("items", {})
    if node.get("options_source") is None:
        raise ValueError('当前字段未配置 options_source')
    return node


def validate_dynamic_options(schema, params, load_options):
    """Require every supplied configured value to match its complete remote list.

    Missing optional fields are not fetched. Cache an item schema's list for this
    validation only; it is not persisted across tasks or accounts.
    """
    cache = {}

    def walk(node, value, field, label):
        if node.get("options_source") is not None:
            key = id(node)
            if key not in cache:
                try:
                    response = load_options(field)
                except ValueError as error:
                    raise OptionsSourceError('解析参数字段选项失败：' + str(error)) from error
                if not isinstance(response, dict) or not isinstance(response.get("items"), list):
                    raise OptionsSourceError('选项响应必须包含 items 数组')
                values = []
                for item in response["items"]:
                    if not isinstance(item, dict) or "value" not in item:
                        raise OptionsSourceError('选项必须包含 value')
                    try:
                        _validate_value(node, item["value"], label)
                    except ParameterValidationError as error:
                        raise OptionsSourceError('选项值不符合字段规则') from error
                    values.append(item["value"])
                cache[key] = values
            if not any(_json_equal(value, option) for option in cache[key]):
                raise ParameterValidationError(label + ': 值不在服务端选项列表中')
        if isinstance(value, dict):
            for name, child in node.get("properties", {}).items():
                if name in value:
                    token = name.replace("~", "~0").replace("/", "~1")
                    walk(child, value[name], field + "/" + token, label + "." + name)
        elif isinstance(value, list) and node.get("items") is not None:
            for index, item in enumerate(value):
                walk(node["items"], item, field + "/" + str(index), label + "[" + str(index) + "]")

    walk(schema, params, "", "params")
