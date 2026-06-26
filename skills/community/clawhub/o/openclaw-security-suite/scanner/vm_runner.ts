import vm from "node:vm"

export function runSandbox(code: string) {

    const context = vm.createContext(Object.create(null))

    const result = vm.runInContext(code, context, {
        timeout: 1000
    })

    return result

}