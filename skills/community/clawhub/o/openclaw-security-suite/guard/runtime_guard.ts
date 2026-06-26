export function runtimeGuard(args: any) {

    if (!args) return

    if (args.url && args.url.includes("169.254.169.254")) {

        throw new Error("Blocked cloud metadata access")

    }

    if (args.command) {

        throw new Error("Shell execution blocked")

    }

}