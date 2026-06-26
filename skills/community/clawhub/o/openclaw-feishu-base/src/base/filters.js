import { z } from 'zod';
import { baseError } from '../errors.js';

export const FilterLeafSchema = z.object({
  field: z.string().min(1),
  operator: z.enum([
    'equals',
    'not_equals',
    'contains',
    'not_contains',
    'starts_with',
    'ends_with',
    'gt',
    'gte',
    'lt',
    'lte',
    'in',
    'not_in',
    'is_empty',
    'is_not_empty',
  ]),
  value: z.unknown().optional(),
});

export const FilterSchema = z.lazy(() =>
  z.union([
    FilterLeafSchema,
    z.object({
      op: z.enum(['and', 'or']),
      conditions: z.array(FilterSchema).min(1),
    }),
  ]),
);

export function compileFilter(filter) {
  if (!filter) return undefined;
  const parsed = FilterSchema.safeParse(filter);
  if (!parsed.success) {
    throw baseError('INVALID_FILTER', 'Invalid filter payload', { issues: parsed.error.issues });
  }
  return toFeishuFilter(parsed.data);
}

function toFeishuFilter(node) {
  if (node?.conditions && node?.op) {
    return {
      conjunction: node.op,
      conditions: [],
      children: node.conditions.map(toFeishuFilter),
    };
  }

  return {
    conjunction: 'and',
    conditions: [toFeishuCondition(node)],
    children: [],
  };
}

function toFeishuCondition(leaf) {
  const operatorMap = {
    equals: 'is',
    not_equals: 'isNot',
    contains: 'contains',
    not_contains: 'doesNotContain',
    starts_with: 'like',
    ends_with: 'like',
    gt: 'isGreater',
    gte: 'isGreaterEqual',
    lt: 'isLess',
    lte: 'isLessEqual',
    in: 'in',
    not_in: 'isNot',
    is_empty: 'isEmpty',
    is_not_empty: 'isNotEmpty',
  };

  const operator = operatorMap[leaf.operator];
  if (!operator) {
    throw baseError('INVALID_FILTER', `Unsupported operator '${leaf.operator}'`);
  }

  let value;
  if (leaf.operator === 'is_empty' || leaf.operator === 'is_not_empty') {
    value = undefined;
  } else if (Array.isArray(leaf.value)) {
    value = leaf.value.map((item) => String(item));
  } else if (leaf.value == null) {
    value = undefined;
  } else if (leaf.operator === 'starts_with') {
    value = [`${String(leaf.value)}%`];
  } else if (leaf.operator === 'ends_with') {
    value = [`%${String(leaf.value)}`];
  } else {
    value = [String(leaf.value)];
  }

  return {
    field_name: leaf.field,
    operator,
    value,
  };
}
