import crypto from "crypto"
import fs from "fs"

export function verifySignature(file: string, signature: string, publicKey: string) {

    const data = fs.readFileSync(file)

    const verify = crypto.createVerify("SHA256")

    verify.update(data)

    return verify.verify(publicKey, signature, "hex")

}