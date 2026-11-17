import { type AccessPolicy } from "../privacy/policy.js";
import type { FilterExpression, OrderBy } from "./client.js";
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
export declare const FILTER_OPERATORS: readonly ["contains", "exact", "begins_with", "ends_with", "regex", "in_list", "greater_than", "less_than"];
export type FilterOperator = (typeof FILTER_OPERATORS)[number];
export type FilterCondition = {
    field: string;
    op: FilterOperator;
    value: string;
};
export type BuiltFilters = {
    dimensionFilter?: FilterExpression;
    metricFilter?: FilterExpression;
    /** One line per condition, so the report says what it was narrowed to. */
    descriptions: string[];
    /**
     * The field names filtered on, in condition order, and nothing else from the
     * condition. The audit log records these; it must never record a value, which
     * is the half that can name a person.
     */
    fields: string[];
};
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
export declare function buildFilters(conditions: readonly FilterCondition[], metrics: readonly string[], policy: AccessPolicy, propertyIdentifying?: ReadonlySet<string>): BuiltFilters;
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
export declare function buildOrderBys(orderBy: string | undefined, metrics: readonly string[], policy: AccessPolicy, propertyIdentifying?: ReadonlySet<string>): OrderBy[] | undefined;
