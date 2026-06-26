import { parse } from "@babel/parser"
import _traverse from "@babel/traverse"
import type { NodePath } from "@babel/traverse"
import type { ImportDeclaration, CallExpression } from "@babel/types"

const traverse = (_traverse as any).default || _traverse

export function astScan(code: string, policy: any) {

    const issues: any[] = []

    const ast = parse(code, {
        sourceType: "module",
        plugins: ["typescript"]
    })

    traverse(ast, {

        ImportDeclaration(path: NodePath<ImportDeclaration>) {

            const moduleName = path.node.source.value

            if (policy.blocked_modules.includes(moduleName)) {

                issues.push({
                    type: "blocked_module",
                    module: moduleName
                })

            }

        },

        CallExpression(path: NodePath<CallExpression>) {

            const callee = path.node.callee

            const name = callee.type === "Identifier" ? callee.name : undefined

            if (name && policy.blocked_functions.includes(name)) {

                issues.push({
                    type: "blocked_function",
                    function: name
                })

            }

        }

    })

    return issues

}