#!/usr/bin/env python3
"""
Activation verifier for home-renovation-planner
Usage: python3 verify_activation.py <activation_code>
Output: VALID or INVALID
"""
import hmac, hashlib, sys, os

SECRET = "d215aad1f5eacbab741fafa529e7b2ca"
MARKER = os.path.expanduser("~/.home-renovation-planner.activated")

# Pre-computed HMAC hashes for valid activation codes
VALID_HASHES = {
    "e265761058f7e24b": "HRP-28ZW-WFBM-9748",
    "41dac6ff4b1167d1": "HRP-2NE6-5QBE-3DCF",
    "d7a32d49bf29a2e4": "HRP-36RB-6VZS-3EK6",
    "54b8dd09d61f83ab": "HRP-4C2K-5DB9-HNWN",
    "ea12ddbda81d44ec": "HRP-4GPJ-9KRU-QGWW",
    "a3503da340104314": "HRP-4WYY-ACJ4-56VB",
    "25e1296a731315d5": "HRP-58TU-EBQX-SZZX",
    "a45ed42e6caaa81f": "HRP-593H-M6JN-47PR",
    "0584e36c16c7a880": "HRP-5MS5-QD7C-QX5C",
    "fcd821cd65559b89": "HRP-5VTE-MPTE-GSMZ",
    "9ffc322ed28bd3b7": "HRP-6DGA-U73S-AAGP",
    "a4d7377c7f8e9f2e": "HRP-6NV5-VJWG-GNKE",
    "82ee850f33e0f0c8": "HRP-6PM5-NV7N-ZSPH",
    "32fcb6d23d51171b": "HRP-6SUN-JNC2-G3PN",
    "9b037d0d884e3cf6": "HRP-6U5Q-2YNP-N8AJ",
    "b1a5669a2b30356a": "HRP-6XM7-8RV9-YNAT",
    "a93a05669d3b1817": "HRP-7PSM-KPTK-V683",
    "7191fd551d8689dc": "HRP-83SC-NS3Y-VD6U",
    "b2275237ca83b24e": "HRP-87X2-GSAW-D28F",
    "acac4105aca4732a": "HRP-894V-6GFY-R4KA",
    "20f4ad4ffbdf6830": "HRP-8A8N-KRPS-WV3U",
    "a23835dc5c47bc62": "HRP-8J7H-GPPK-727F",
    "f35936b12694d251": "HRP-8Q4G-WETJ-HG6E",
    "dcb6ad953a6e3666": "HRP-8UKU-TTK8-X789",
    "f5780f6dadd0f3ce": "HRP-A56J-QPAJ-PZPT",
    "1feb539a41cb7fa0": "HRP-A72V-YNWA-Z6CZ",
    "ba3bad27cb2fed70": "HRP-AF22-CAUY-NSUN",
    "b753a572d9ba7c6b": "HRP-AJEQ-E7RA-7KTA",
    "36ef4aa33ba7966b": "HRP-ANUW-KD9D-HJDF",
    "b7fb16157e9a4cce": "HRP-ASE2-H3GB-WWXF",
    "e139d41764a36a8f": "HRP-ATRY-4VN6-HZCE",
    "3ded635560d6bb59": "HRP-ATVU-Y49A-JXXT",
    "72f57268308be7ba": "HRP-B2AR-SHRC-3QNH",
    "9e45a0e098e82af4": "HRP-B99R-8KKG-PQM6",
    "d9f06be26ab796f4": "HRP-BDXC-Q257-NMWY",
    "855f1df4ffa2bfd2": "HRP-BJZK-2VHC-EE3M",
    "f0324f2e54ba91c7": "HRP-BKHZ-XRN4-MK52",
    "b6743daf5c121dea": "HRP-CTQR-5U27-VYJ3",
    "e7acf2a1fd75e522": "HRP-CUQJ-BX46-YKHA",
    "3cd80b70e850acc1": "HRP-D5FJ-BNFP-7HTD",
    "0e7de5dc4cccd3a8": "HRP-DA7T-NCXC-M3D2",
    "b48167f72d4607f0": "HRP-DD9D-XTEJ-252G",
    "caf3030390126ef3": "HRP-DDPU-6MWB-AB59",
    "961e4ff476b3ecc2": "HRP-DMB7-H67X-B6V2",
    "50c4d26c946e4d59": "HRP-DSEG-5KU5-6ESJ",
    "4515e296e83459ae": "HRP-DTGC-KWGK-B34E",
    "b25de4dbdcb0dba5": "HRP-E8YJ-2XXD-6WYP",
    "7a7e32cc5c359337": "HRP-EREQ-32ZV-WE4P",
    "420b066f68ebd312": "HRP-FQNZ-MKQE-5X84",
    "8683597c933bc6b4": "HRP-FYY2-TCQX-W432",
    "6963c486ad25be62": "HRP-G8W8-DE6T-MAUG",
    "8b51ab26c9f3c8c8": "HRP-GBJE-E8AX-XY4Z",
    "1aea17f2fcc769d8": "HRP-GFSY-HMUM-RBY5",
    "b390e4714160ee25": "HRP-GHZ9-XBGZ-CBCH",
    "e57149920f999730": "HRP-GM4T-78DA-MPMA",
    "0f663ba58fe999b4": "HRP-GNZV-BX5A-ARCT",
    "25e12bcaf8044479": "HRP-GTN8-K47N-4B9Q",
    "1badce2c940e8877": "HRP-H2XF-5WQH-NFZS",
    "543ba904697ed6f3": "HRP-H694-8WP4-YPFN",
    "81c4b2eb15efdfb3": "HRP-HAFA-2C6D-5S9Y",
    "42f47eb7985868da": "HRP-HH6K-UWEJ-UT7M",
    "c33da23f1efff686": "HRP-J2PC-RJG5-464X",
    "548712a23fee5b5f": "HRP-JN9D-4ZTT-5E77",
    "168cb6e57d4349c8": "HRP-K67X-FSY3-VKUA",
    "11a15ea325bd3b1d": "HRP-KD9G-BZ9U-AYVF",
    "9c2e7b03f15d2e57": "HRP-KUWW-65RQ-AKSR",
    "18ae3821ec19a922": "HRP-M784-4FJV-HS6Z",
    "0b9e550182655128": "HRP-MXWB-JFE7-QRGS",
    "9cb35d9285cb507e": "HRP-NHT8-TPGD-3USV",
    "7a826b2f6cbde522": "HRP-NJCH-RVFC-JXGU",
    "7f7fc8fa8beff302": "HRP-NP59-YXMF-CYYQ",
    "981fe0f65a97c2d4": "HRP-PT9W-CYBM-VWHW",
    "5259ad910fe170bb": "HRP-QF7C-E9G9-QCT7",
    "43cab9b644e48dfd": "HRP-QKAM-S46J-YADV",
    "56de7fe4ce81acf3": "HRP-QPJU-FKJX-FWBS",
    "b27953f11c0aee05": "HRP-QXCW-RCWJ-NVPG",
    "6117245ddb8ae9de": "HRP-R5KQ-MR9U-ZY5J",
    "d11ddb3ae1e5f186": "HRP-RJ3M-29FU-RRH9",
    "eb46500e4f6679d7": "HRP-RQ8A-CSAE-FAVA",
    "d1b5469aa730c513": "HRP-SS5U-KCW9-U7TU",
    "1807e1d572b8744d": "HRP-TCBE-74QS-RXPN",
    "25aa643947f02b83": "HRP-U2A5-4ETW-6F8B",
    "eb675307e7a2e535": "HRP-UCN2-HAYK-Z6R4",
    "6b9b4c125c9b7c3f": "HRP-UHVK-K2ZX-BCKP",
    "b02ec934fc6abd70": "HRP-UKGK-5SJV-JNN2",
    "a09e5519f243d526": "HRP-V3BX-THG9-SE9S",
    "06d33aaca177e76d": "HRP-V3GZ-5SSG-JFQ9",
    "10a8d80811a6c7c9": "HRP-VVF3-MT8R-SYDQ",
    "dd5fb3965d3f5388": "HRP-VXQ7-ZEF8-QPS8",
    "1a41396d02b71185": "HRP-W5RA-BV7B-CJVF",
    "55886155d02439c6": "HRP-WACS-4KAR-7S3M",
    "cec5fddcfbe0c22c": "HRP-WBBW-BDCY-GHZ9",
    "ee12664bbcf27898": "HRP-WWC9-T8FH-4P5Y",
    "384f8ebed8ea8bf1": "HRP-XKKQ-KAGU-Y68H",
    "1c7561d16d3fd166": "HRP-Y826-24PB-EXFD",
    "48ae81247e296996": "HRP-YECY-WGSC-NVY7",
    "2ece725968d78f4f": "HRP-YHEH-MK43-DNH9",
    "e15fd75fb4c6b33a": "HRP-YPC2-HEWT-5BCB",
    "4735a615076615c7": "HRP-Z3PC-XDZE-RUHC",
    "7859497c61616549": "HRP-ZWVC-RW2R-G2K7",
}


def verify(code):
    code = code.strip().upper()
    h = hmac.new(SECRET.encode(), code.encode(), hashlib.sha256).hexdigest()[:16]
    if h in VALID_HASHES:
        return True
    return False

def main():
    if len(sys.argv) != 2:
        print("INVALID")
        sys.exit(0)
    
    code = sys.argv[1].strip()
    
    if verify(code):
        with open(MARKER, "w") as f:
            f.write(code)
        print("VALID")
        sys.exit(0)
    
    print("INVALID")
    sys.exit(0)

if __name__ == "__main__":
    main()
