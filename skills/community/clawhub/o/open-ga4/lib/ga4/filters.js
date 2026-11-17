import { assertDimensionsAllowed } from "../privacy/policy.js";
import { flattenNewlines } from "./format.js";
import { Ga4RequestError } from "./limits.js";
/**
 * A small filter vocabulary for the `query` command.
 *
 * Deliberately narrower than the API's full `FilterExpression` tree. A model
 * composing nested and/or/not groups from a free-form schema gets it wrong
 * often; a flat list of conditions combined with AND covers what people
 * actually ask for and can be validated completely before a request is spent.
 *
 * A filter that cannot be built raises. It is never silently dropped; a
 * filtered question that quietly returns whole-site numbers is worse than an
 * error, because the number looks right.
 */
export const FILTER_OPERATORS = [
    "contains",
    "exact",
    "begins_with",
    "ends_with",
    "regex",
    "in_list",
    "greater_than",
    "less_than",
];
const STRING_MATCH = {
    contains: "CONTAINS",
    exact: "EXACT",
    begins_with: "BEGINS_WITH",
    ends_with: "ENDS_WITH",
    regex: "FULL_REGEXP",
};
const NUMERIC_OPERATION = {
    greater_than: "GREATER_THAN",
    less_than: "LESS_THAN",
};
function buildOne(condition, isMetric) {
    const { field, op, value } = condition;
    const numericOperation = NUMERIC_OPERATION[op];
    if (numericOperation) {
        const numeric = Number(value);
        if (!Number.isFinite(numeric)) {
            throw new Ga4RequestError("BAD_FILTER_VALUE", `Filter "${field} ${op} ${value}" needs a number, and "${value}" is not one.`);
        }
        return {
            filter: {
                fieldName: field,
                numericFilter: { operation: numericOperation, value: { doubleValue: numeric } },
            },
        };
    }
    if (isMetric) {
        throw new Ga4RequestError("BAD_FILTER_OPERATOR", `${field} is a metric, so it can only be filtered with greater_than or less_than, ` +
            `not "${op}". Filter a dimension by text instead, or compare the metric numerically.`);
    }
    if (op === "in_list") {
        const values = value
            .split(",")
            .map((entry) => entry.trim())
            .filter((entry) => entry.length > 0);
        if (values.length === 0) {
            throw new Ga4RequestError("BAD_FILTER_VALUE", `Filter "${field} in_list" needs a comma-separated list of values.`);
        }
        return { filter: { fieldName: field, inListFilter: { values, caseSensitive: false } } };
    }
    if (op === "regex") {
        try {
            new RegExp(value);
        }
        catch (error) {
            throw new Ga4RequestError("BAD_FILTER_VALUE", `Filter "${field} regex" is not a valid regular expression: ` +
                `${error instanceof Error ? error.message : String(error)}`);
        }
    }
    const matchType = STRING_MATCH[op];
    if (!matchType) {
        throw new Ga4RequestError("BAD_FILTER_OPERATOR", `Unknown filter operator "${op}". Available: ${FILTER_OPERATORS.join(", ")}.`);
    }
    return {
        filter: { fieldName: field, stringFilter: { matchType, value, caseSensitive: false } },
    };
}
/**
 * Split conditions into the dimension and metric filters the API expects, and
 * combine each side with AND.
 *
 * The privacy policy is enforced here rather than at the call site, because a
 * filter field is a dimension name and this is the only place one can become
 * part of a request. Checking it in `runQuery` would leave the check one
 * copy-paste away from being missed: the defect this closes was precisely a
 * gate that ran on the dimension list `runQuery` passed to Google and not on
 * the filter fields it passed alongside them, so `--dimensions userId` was
 * refused while `--filter userId:exact:<a person>` was not, and the response
 * looked like an ordinary page report. Requiring the policy as an argument
 * makes it impossible to add a caller that quietly skips it.
 */
export function buildFilters(conditions, metrics, policy, propertyIdentifying = new Set()) {
    assertDimensionsAllowed(conditions.filter((condition) => !metrics.includes(condition.field)).map((c) => c.field), policy, propertyIdentifying, "filter");
    const dimensionSide = [];
    const metricSide = [];
    const descriptions = [];
    for (const condition of conditions) {
        const isMetric = metrics.includes(condition.field);
        const expression = buildOne(condition, isMetric);
        (isMetric ? metricSide : dimensionSide).push(expression);
        // Flattened, because this description is the one piece of caller-supplied
        // text that ends up in prose rather than inside the fenced block a report's
        // rows live in. A newline here would start a line of its own in the
        // caveats list, which reads differently to a model than the same text
        // mid-sentence.
        descriptions.push(`${flattenNewlines(condition.field)} ${condition.op.replace(/_/g, " ")} ` +
            `"${flattenNewlines(condition.value)}"`);
    }
    const combine = (list) => {
        if (list.length === 0)
            return undefined;
        if (list.length === 1)
            return list[0];
        return { andGroup: { expressions: list } };
    };
    return {
        ...(combine(dimensionSide) ? { dimensionFilter: combine(dimensionSide) } : {}),
        ...(combine(metricSide) ? { metricFilter: combine(metricSide) } : {}),
        descriptions,
        fields: conditions.map((condition) => condition.field),
    };
}
/**
 * The sort key, as the metric or dimension ordering the API expects.
 *
 * Here, next to buildFilters, for the same reason and against the same defect:
 * a sort key is the second channel that carries a dimension name into a request
 * without it ever appearing as a column, so `--sort userId` reached the wire
 * unchecked while `--dimensions userId` was refused. Anything that needs to
 * order a report gets the policy check by construction rather than by
 * remembering.
 */
export function buildOrderBys(orderBy, metrics, policy, propertyIdentifying = new Set()) {
    if (!orderBy) {
        return undefined;
    }
    if (metrics.includes(orderBy)) {
        return [{ desc: true, metric: { metricName: orderBy } }];
    }
    assertDimensionsAllowed([orderBy], policy, propertyIdentifying, "sort");
    return [{ desc: true, dimension: { dimensionName: orderBy } }];
}
