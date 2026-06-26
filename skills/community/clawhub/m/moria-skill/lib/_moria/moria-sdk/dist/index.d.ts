import { PublicKey, Connection, TransactionInstruction, Transaction, Commitment } from '@solana/web3.js';
import { Accounts, IdlTypes, IdlAccounts, BN, Program } from '@coral-xyz/anchor';
import BN$1 from 'bn.js';

/**
 * Program IDL in camelCase format in order to be used in JS/TS.
 *
 * Note that this is only a type helper and is not the actual IDL. The original
 * IDL can be found at `target/idl/clawlab.json`.
 */
type Clawlab = {
    "address": "J88VV7gYpBiV2nqt3mUeAwc9hCgB6YoVmqaVAamJRTb7";
    "metadata": {
        "name": "clawlab";
        "version": "0.1.0";
        "spec": "0.1.0";
        "description": "Created with Anchor";
    };
    "instructions": [
        {
            "name": "buyToken";
            "discriminator": [
                138,
                127,
                14,
                91,
                38,
                87,
                115,
                105
            ];
            "accounts": [
                {
                    "name": "payer";
                    "writable": true;
                    "signer": true;
                },
                {
                    "name": "poolAuthority";
                    "address": "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB";
                },
                {
                    "name": "config";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    99,
                                    111,
                                    110,
                                    102,
                                    105,
                                    103
                                ];
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "baseMint";
                    "writable": true;
                },
                {
                    "name": "quoteMint";
                },
                {
                    "name": "pool";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    112,
                                    111,
                                    111,
                                    108
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "baseMint";
                            },
                            {
                                "kind": "account";
                                "path": "quoteMint";
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "baseVault";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    98,
                                    97,
                                    115,
                                    101,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "config";
                            },
                            {
                                "kind": "account";
                                "path": "baseMint";
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "quoteVault";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    113,
                                    117,
                                    111,
                                    116,
                                    101,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "config";
                            },
                            {
                                "kind": "account";
                                "path": "quoteMint";
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "inputTokenAccount";
                    "writable": true;
                },
                {
                    "name": "outputTokenAccount";
                    "writable": true;
                },
                {
                    "name": "userTokenAccount";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    117,
                                    115,
                                    101,
                                    114,
                                    95,
                                    116,
                                    111,
                                    107,
                                    101,
                                    110,
                                    95,
                                    97,
                                    99,
                                    99,
                                    111,
                                    117,
                                    110,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "baseMint";
                            },
                            {
                                "kind": "account";
                                "path": "payer";
                            }
                        ];
                    };
                },
                {
                    "name": "tokenBaseProgram";
                },
                {
                    "name": "tokenQuoteProgram";
                },
                {
                    "name": "systemProgram";
                    "address": "11111111111111111111111111111111";
                },
                {
                    "name": "eventAuthority";
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    "name": "program";
                }
            ];
            "args": [
                {
                    "name": "parameters";
                    "type": {
                        "defined": {
                            "name": "buyTokenParameters";
                        };
                    };
                }
            ];
        },
        {
            "name": "claimAuthority";
            "discriminator": [
                222,
                132,
                185,
                123,
                127,
                107,
                6,
                31
            ];
            "accounts": [
                {
                    "name": "payer";
                    "writable": true;
                    "signer": true;
                },
                {
                    "name": "poolAuthority";
                    "writable": true;
                    "address": "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB";
                },
                {
                    "name": "systemProgram";
                    "address": "11111111111111111111111111111111";
                },
                {
                    "name": "eventAuthority";
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    "name": "program";
                }
            ];
            "args": [];
        },
        {
            "name": "claimCpammPool";
            "discriminator": [
                68,
                75,
                169,
                205,
                40,
                228,
                159,
                101
            ];
            "accounts": [
                {
                    "name": "payer";
                    "writable": true;
                    "signer": true;
                },
                {
                    "name": "poolAuthority";
                    "address": "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB";
                },
                {
                    "name": "config";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    99,
                                    111,
                                    110,
                                    102,
                                    105,
                                    103
                                ];
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "baseMint";
                    "writable": true;
                },
                {
                    "name": "quoteMint";
                },
                {
                    "name": "pool";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    112,
                                    111,
                                    111,
                                    108
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "baseMint";
                            },
                            {
                                "kind": "account";
                                "path": "quoteMint";
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "baseVault";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    98,
                                    97,
                                    115,
                                    101,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "config";
                            },
                            {
                                "kind": "account";
                                "path": "baseMint";
                            }
                        ];
                    };
                },
                {
                    "name": "quoteVault";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    113,
                                    117,
                                    111,
                                    116,
                                    101,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "config";
                            },
                            {
                                "kind": "account";
                                "path": "quoteMint";
                            }
                        ];
                    };
                },
                {
                    "name": "tokenBaseProgram";
                },
                {
                    "name": "tokenQuoteProgram";
                },
                {
                    "name": "cpAmmPoolAuthority";
                    "docs": [
                        "meteora"
                    ];
                },
                {
                    "name": "cpAmmPool";
                },
                {
                    "name": "cpAmmPosition";
                    "writable": true;
                },
                {
                    "name": "cpAmmTokenAVault";
                    "writable": true;
                },
                {
                    "name": "cpAmmTokenBVault";
                    "writable": true;
                },
                {
                    "name": "cpAmmPositionNftAccount";
                },
                {
                    "name": "cpAmmEventAuthority";
                },
                {
                    "name": "cpAmmProgram";
                    "address": "cpamdpZCGKUy5JxQXB4dcpGPiikHawvSWAd6mEn1sGG";
                },
                {
                    "name": "eventAuthority";
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    "name": "program";
                }
            ];
            "args": [
                {
                    "name": "parameters";
                    "type": {
                        "defined": {
                            "name": "claimCpAmmPoolParameters";
                        };
                    };
                }
            ];
        },
        {
            "name": "claimCreator";
            "discriminator": [
                231,
                240,
                197,
                249,
                244,
                10,
                21,
                59
            ];
            "accounts": [
                {
                    "name": "payer";
                    "writable": true;
                    "signer": true;
                },
                {
                    "name": "poolAuthority";
                    "address": "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB";
                },
                {
                    "name": "config";
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    99,
                                    111,
                                    110,
                                    102,
                                    105,
                                    103
                                ];
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "pool";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    112,
                                    111,
                                    111,
                                    108
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "baseMint";
                            },
                            {
                                "kind": "account";
                                "path": "quoteMint";
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "baseMint";
                    "writable": true;
                },
                {
                    "name": "quoteMint";
                },
                {
                    "name": "quoteVault";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    113,
                                    117,
                                    111,
                                    116,
                                    101,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "config";
                            },
                            {
                                "kind": "account";
                                "path": "quoteMint";
                            }
                        ];
                    };
                },
                {
                    "name": "tokenAccount";
                    "docs": [
                        "The user token account for output token"
                    ];
                    "writable": true;
                },
                {
                    "name": "tokenBaseProgram";
                },
                {
                    "name": "tokenQuoteProgram";
                },
                {
                    "name": "eventAuthority";
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    "name": "program";
                }
            ];
            "args": [];
        },
        {
            "name": "claimPrize";
            "discriminator": [
                157,
                233,
                139,
                121,
                246,
                62,
                234,
                235
            ];
            "accounts": [
                {
                    "name": "payer";
                    "writable": true;
                    "signer": true;
                },
                {
                    "name": "poolAuthority";
                    "address": "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB";
                },
                {
                    "name": "config";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    99,
                                    111,
                                    110,
                                    102,
                                    105,
                                    103
                                ];
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "quoteMint";
                },
                {
                    "name": "quoteVault";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    113,
                                    117,
                                    111,
                                    116,
                                    101,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "config";
                            },
                            {
                                "kind": "account";
                                "path": "quoteMint";
                            }
                        ];
                    };
                },
                {
                    "name": "tokenAccount";
                    "docs": [
                        "The user token account for output token"
                    ];
                    "writable": true;
                },
                {
                    "name": "tokenQuoteProgram";
                },
                {
                    "name": "eventAuthority";
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    "name": "program";
                }
            ];
            "args": [];
        },
        {
            "name": "claimProtocol";
            "discriminator": [
                230,
                39,
                79,
                248,
                193,
                76,
                247,
                53
            ];
            "accounts": [
                {
                    "name": "payer";
                    "writable": true;
                    "signer": true;
                },
                {
                    "name": "poolAuthority";
                    "address": "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB";
                },
                {
                    "name": "config";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    99,
                                    111,
                                    110,
                                    102,
                                    105,
                                    103
                                ];
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "quoteMint";
                },
                {
                    "name": "quoteVault";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    113,
                                    117,
                                    111,
                                    116,
                                    101,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "config";
                            },
                            {
                                "kind": "account";
                                "path": "quoteMint";
                            }
                        ];
                    };
                },
                {
                    "name": "tokenAccount";
                    "docs": [
                        "The user token account for output token"
                    ];
                    "writable": true;
                },
                {
                    "name": "tokenQuoteProgram";
                },
                {
                    "name": "eventAuthority";
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    "name": "program";
                }
            ];
            "args": [];
        },
        {
            "name": "claimUserToken";
            "discriminator": [
                164,
                41,
                212,
                48,
                37,
                95,
                41,
                109
            ];
            "accounts": [
                {
                    "name": "payer";
                    "writable": true;
                    "signer": true;
                },
                {
                    "name": "poolAuthority";
                    "address": "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB";
                },
                {
                    "name": "baseMint";
                    "writable": true;
                },
                {
                    "name": "quoteMint";
                },
                {
                    "name": "pool";
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    112,
                                    111,
                                    111,
                                    108
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "baseMint";
                            },
                            {
                                "kind": "account";
                                "path": "quoteMint";
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "inputTokenAccount";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    117,
                                    115,
                                    101,
                                    114,
                                    95,
                                    116,
                                    111,
                                    107,
                                    101,
                                    110,
                                    95,
                                    97,
                                    99,
                                    99,
                                    111,
                                    117,
                                    110,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "baseMint";
                            },
                            {
                                "kind": "account";
                                "path": "payer";
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "outputTokenAccount";
                    "docs": [
                        "The user token account for output token"
                    ];
                    "writable": true;
                },
                {
                    "name": "tokenBaseProgram";
                },
                {
                    "name": "tokenQuoteProgram";
                },
                {
                    "name": "eventAuthority";
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    "name": "program";
                }
            ];
            "args": [];
        },
        {
            "name": "claimUserToken1";
            "discriminator": [
                163,
                250,
                62,
                164,
                192,
                163,
                227,
                147
            ];
            "accounts": [
                {
                    "name": "payer";
                    "writable": true;
                    "signer": true;
                },
                {
                    "name": "poolAuthority";
                    "address": "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB";
                },
                {
                    "name": "baseMint";
                    "writable": true;
                },
                {
                    "name": "quoteMint";
                },
                {
                    "name": "pool";
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    112,
                                    111,
                                    111,
                                    108
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "baseMint";
                            },
                            {
                                "kind": "account";
                                "path": "quoteMint";
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "inputTokenAccount";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    117,
                                    115,
                                    101,
                                    114,
                                    95,
                                    116,
                                    111,
                                    107,
                                    101,
                                    110,
                                    95,
                                    97,
                                    99,
                                    99,
                                    111,
                                    117,
                                    110,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "baseMint";
                            },
                            {
                                "kind": "account";
                                "path": "owner";
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "outputTokenAccount";
                    "docs": [
                        "The user token account for output token"
                    ];
                    "writable": true;
                },
                {
                    "name": "owner";
                },
                {
                    "name": "tokenBaseProgram";
                },
                {
                    "name": "tokenQuoteProgram";
                },
                {
                    "name": "eventAuthority";
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    "name": "program";
                }
            ];
            "args": [];
        },
        {
            "name": "initializeConfig";
            "discriminator": [
                208,
                127,
                21,
                1,
                194,
                190,
                196,
                70
            ];
            "accounts": [
                {
                    "name": "poolAuthority";
                    "address": "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB";
                },
                {
                    "name": "config";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    99,
                                    111,
                                    110,
                                    102,
                                    105,
                                    103
                                ];
                            }
                        ];
                    };
                },
                {
                    "name": "quoteMint";
                },
                {
                    "name": "quoteVault";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    113,
                                    117,
                                    111,
                                    116,
                                    101,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "config";
                            },
                            {
                                "kind": "account";
                                "path": "quoteMint";
                            }
                        ];
                    };
                },
                {
                    "name": "payer";
                    "writable": true;
                    "signer": true;
                },
                {
                    "name": "tokenQuoteProgram";
                    "docs": [
                        "Program to create mint account and mint tokens"
                    ];
                },
                {
                    "name": "systemProgram";
                    "address": "11111111111111111111111111111111";
                }
            ];
            "args": [];
        },
        {
            "name": "initializeSplPool";
            "discriminator": [
                220,
                77,
                162,
                14,
                209,
                171,
                12,
                200
            ];
            "accounts": [
                {
                    "name": "poolAuthority";
                    "address": "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB";
                },
                {
                    "name": "config";
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    99,
                                    111,
                                    110,
                                    102,
                                    105,
                                    103
                                ];
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "baseMint";
                    "writable": true;
                    "signer": true;
                },
                {
                    "name": "quoteMint";
                },
                {
                    "name": "pool";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    112,
                                    111,
                                    111,
                                    108
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "baseMint";
                            },
                            {
                                "kind": "account";
                                "path": "quoteMint";
                            }
                        ];
                    };
                },
                {
                    "name": "baseVault";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    98,
                                    97,
                                    115,
                                    101,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "config";
                            },
                            {
                                "kind": "account";
                                "path": "baseMint";
                            }
                        ];
                    };
                },
                {
                    "name": "quoteVault";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    113,
                                    117,
                                    111,
                                    116,
                                    101,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "config";
                            },
                            {
                                "kind": "account";
                                "path": "quoteMint";
                            }
                        ];
                    };
                },
                {
                    "name": "mintMetadata";
                    "writable": true;
                },
                {
                    "name": "metadataProgram";
                    "address": "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s";
                },
                {
                    "name": "payer";
                    "writable": true;
                    "signer": true;
                },
                {
                    "name": "tokenBaseProgram";
                },
                {
                    "name": "tokenQuoteProgram";
                },
                {
                    "name": "systemProgram";
                    "address": "11111111111111111111111111111111";
                },
                {
                    "name": "eventAuthority";
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    "name": "program";
                }
            ];
            "args": [
                {
                    "name": "parameters";
                    "type": {
                        "defined": {
                            "name": "initializePoolParameters";
                        };
                    };
                }
            ];
        },
        {
            "name": "migrationToken";
            "discriminator": [
                29,
                61,
                122,
                95,
                208,
                221,
                166,
                184
            ];
            "accounts": [
                {
                    "name": "payer";
                    "writable": true;
                    "signer": true;
                },
                {
                    "name": "poolAuthority";
                    "writable": true;
                    "address": "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB";
                },
                {
                    "name": "config";
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    99,
                                    111,
                                    110,
                                    102,
                                    105,
                                    103
                                ];
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "baseMint";
                    "writable": true;
                },
                {
                    "name": "quoteMint";
                },
                {
                    "name": "pool";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    112,
                                    111,
                                    111,
                                    108
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "baseMint";
                            },
                            {
                                "kind": "account";
                                "path": "quoteMint";
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "baseVault";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    98,
                                    97,
                                    115,
                                    101,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "config";
                            },
                            {
                                "kind": "account";
                                "path": "baseMint";
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "quoteVault";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    113,
                                    117,
                                    111,
                                    116,
                                    101,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "config";
                            },
                            {
                                "kind": "account";
                                "path": "quoteMint";
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "tokenQuoteProgram";
                },
                {
                    "name": "tokenBaseProgram";
                },
                {
                    "name": "systemProgram";
                    "address": "11111111111111111111111111111111";
                },
                {
                    "name": "cpAmmPositionNftMint";
                    "docs": [
                        "meteora"
                    ];
                    "writable": true;
                    "signer": true;
                },
                {
                    "name": "cpAmmPositionNftAccount";
                    "writable": true;
                },
                {
                    "name": "cpAmmPoolAuthority";
                },
                {
                    "name": "cpAmmPool";
                    "writable": true;
                },
                {
                    "name": "cpAmmPosition";
                    "writable": true;
                },
                {
                    "name": "cpAmmTokenAVault";
                    "writable": true;
                },
                {
                    "name": "cpAmmTokenBVault";
                    "writable": true;
                },
                {
                    "name": "token2022Program";
                    "address": "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb";
                },
                {
                    "name": "cpAmmEventAuthority";
                },
                {
                    "name": "cpAmmProgram";
                    "address": "cpamdpZCGKUy5JxQXB4dcpGPiikHawvSWAd6mEn1sGG";
                },
                {
                    "name": "eventAuthority";
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    "name": "program";
                }
            ];
            "args": [
                {
                    "name": "parameters";
                    "type": {
                        "defined": {
                            "name": "migrationTokenParameters";
                        };
                    };
                }
            ];
        },
        {
            "name": "refundToken";
            "discriminator": [
                198,
                194,
                93,
                209,
                12,
                211,
                46,
                174
            ];
            "accounts": [
                {
                    "name": "payer";
                    "writable": true;
                    "signer": true;
                },
                {
                    "name": "poolAuthority";
                    "address": "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB";
                },
                {
                    "name": "config";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    99,
                                    111,
                                    110,
                                    102,
                                    105,
                                    103
                                ];
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "baseMint";
                    "writable": true;
                },
                {
                    "name": "quoteMint";
                },
                {
                    "name": "pool";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    112,
                                    111,
                                    111,
                                    108
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "baseMint";
                            },
                            {
                                "kind": "account";
                                "path": "quoteMint";
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "baseVault";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    98,
                                    97,
                                    115,
                                    101,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "config";
                            },
                            {
                                "kind": "account";
                                "path": "baseMint";
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "quoteVault";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    113,
                                    117,
                                    111,
                                    116,
                                    101,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "config";
                            },
                            {
                                "kind": "account";
                                "path": "quoteMint";
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "inputTokenAccount";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    117,
                                    115,
                                    101,
                                    114,
                                    95,
                                    116,
                                    111,
                                    107,
                                    101,
                                    110,
                                    95,
                                    97,
                                    99,
                                    99,
                                    111,
                                    117,
                                    110,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "baseMint";
                            },
                            {
                                "kind": "account";
                                "path": "payer";
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "outputTokenAccount";
                    "writable": true;
                },
                {
                    "name": "tokenQuoteProgram";
                },
                {
                    "name": "tokenBaseProgram";
                },
                {
                    "name": "systemProgram";
                    "address": "11111111111111111111111111111111";
                },
                {
                    "name": "eventAuthority";
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    "name": "program";
                }
            ];
            "args": [];
        },
        {
            "name": "refundToken1";
            "discriminator": [
                139,
                18,
                167,
                208,
                174,
                17,
                74,
                73
            ];
            "accounts": [
                {
                    "name": "payer";
                    "writable": true;
                    "signer": true;
                },
                {
                    "name": "poolAuthority";
                    "address": "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB";
                },
                {
                    "name": "config";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    99,
                                    111,
                                    110,
                                    102,
                                    105,
                                    103
                                ];
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "baseMint";
                    "writable": true;
                },
                {
                    "name": "quoteMint";
                },
                {
                    "name": "pool";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    112,
                                    111,
                                    111,
                                    108
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "baseMint";
                            },
                            {
                                "kind": "account";
                                "path": "quoteMint";
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "baseVault";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    98,
                                    97,
                                    115,
                                    101,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "config";
                            },
                            {
                                "kind": "account";
                                "path": "baseMint";
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "quoteVault";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    113,
                                    117,
                                    111,
                                    116,
                                    101,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "config";
                            },
                            {
                                "kind": "account";
                                "path": "quoteMint";
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "inputTokenAccount";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    117,
                                    115,
                                    101,
                                    114,
                                    95,
                                    116,
                                    111,
                                    107,
                                    101,
                                    110,
                                    95,
                                    97,
                                    99,
                                    99,
                                    111,
                                    117,
                                    110,
                                    116
                                ];
                            },
                            {
                                "kind": "account";
                                "path": "baseMint";
                            },
                            {
                                "kind": "account";
                                "path": "owner";
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                },
                {
                    "name": "outputTokenAccount";
                    "writable": true;
                },
                {
                    "name": "owner";
                },
                {
                    "name": "tokenQuoteProgram";
                },
                {
                    "name": "tokenBaseProgram";
                },
                {
                    "name": "systemProgram";
                    "address": "11111111111111111111111111111111";
                },
                {
                    "name": "eventAuthority";
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    "name": "program";
                }
            ];
            "args": [];
        },
        {
            "name": "setFee";
            "discriminator": [
                18,
                154,
                24,
                18,
                237,
                214,
                19,
                80
            ];
            "accounts": [
                {
                    "name": "payer";
                    "writable": true;
                    "signer": true;
                },
                {
                    "name": "config";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    99,
                                    111,
                                    110,
                                    102,
                                    105,
                                    103
                                ];
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                }
            ];
            "args": [
                {
                    "name": "parameters";
                    "type": {
                        "defined": {
                            "name": "setFeeParameters";
                        };
                    };
                }
            ];
        },
        {
            "name": "setIsOpen";
            "discriminator": [
                18,
                178,
                20,
                101,
                216,
                109,
                120,
                91
            ];
            "accounts": [
                {
                    "name": "payer";
                    "writable": true;
                    "signer": true;
                },
                {
                    "name": "config";
                    "writable": true;
                    "pda": {
                        "seeds": [
                            {
                                "kind": "const";
                                "value": [
                                    99,
                                    111,
                                    110,
                                    102,
                                    105,
                                    103
                                ];
                            }
                        ];
                        "program": {
                            "kind": "const";
                            "value": [
                                254,
                                106,
                                54,
                                177,
                                90,
                                171,
                                158,
                                137,
                                49,
                                48,
                                101,
                                188,
                                131,
                                121,
                                2,
                                228,
                                234,
                                190,
                                158,
                                169,
                                183,
                                92,
                                174,
                                94,
                                103,
                                171,
                                130,
                                147,
                                18,
                                20,
                                41,
                                114
                            ];
                        };
                    };
                }
            ];
            "args": [
                {
                    "name": "parameters";
                    "type": {
                        "defined": {
                            "name": "setIsOpenParameters";
                        };
                    };
                }
            ];
        }
    ];
    "accounts": [
        {
            "name": "config";
            "discriminator": [
                155,
                12,
                170,
                224,
                30,
                250,
                204,
                130
            ];
        },
        {
            "name": "poolConfig";
            "discriminator": [
                26,
                108,
                14,
                123,
                116,
                230,
                129,
                43
            ];
        }
    ];
    "events": [
        {
            "name": "evtBuy";
            "discriminator": [
                17,
                72,
                229,
                72,
                199,
                251,
                146,
                52
            ];
        },
        {
            "name": "evtComplete";
            "discriminator": [
                226,
                27,
                174,
                149,
                122,
                226,
                53,
                26
            ];
        },
        {
            "name": "evtCreate";
            "discriminator": [
                161,
                151,
                143,
                156,
                214,
                22,
                51,
                176
            ];
        },
        {
            "name": "evtIncomplete";
            "discriminator": [
                220,
                102,
                179,
                92,
                97,
                70,
                196,
                230
            ];
        },
        {
            "name": "evtLiquidityAdded";
            "discriminator": [
                179,
                26,
                205,
                20,
                216,
                117,
                57,
                101
            ];
        },
        {
            "name": "evtRefund";
            "discriminator": [
                117,
                182,
                71,
                97,
                117,
                66,
                212,
                43
            ];
        }
    ];
    "errors": [
        {
            "code": 6000;
            "name": "mathOverflow";
        },
        {
            "code": 6001;
            "name": "invalidFee";
        },
        {
            "code": 6002;
            "name": "exceededSlippage";
        },
        {
            "code": 6003;
            "name": "poolDisabled";
        },
        {
            "code": 6004;
            "name": "exceedMaxFeeBps";
        },
        {
            "code": 6005;
            "name": "invalidAdmin";
        },
        {
            "code": 6006;
            "name": "amountIsZero";
        },
        {
            "code": 6007;
            "name": "typeCastFailed";
        },
        {
            "code": 6008;
            "name": "unableToModifyActivationPoint";
        },
        {
            "code": 6009;
            "name": "invalidAuthorityToCreateThePool";
        },
        {
            "code": 6010;
            "name": "invalidActivationType";
        },
        {
            "code": 6011;
            "name": "invalidActivationPoint";
        },
        {
            "code": 6012;
            "name": "invalidQuoteMint";
        },
        {
            "code": 6013;
            "name": "invalidFeeCurve";
        },
        {
            "code": 6014;
            "name": "invalidPriceRange";
        },
        {
            "code": 6015;
            "name": "priceRangeViolation";
        },
        {
            "code": 6016;
            "name": "invalidParameters";
        },
        {
            "code": 6017;
            "name": "invalidCollectFeeMode";
        },
        {
            "code": 6018;
            "name": "invalidInput";
        },
        {
            "code": 6019;
            "name": "cannotCreateTokenBadgeOnSupportedMint";
        },
        {
            "code": 6020;
            "name": "invalidTokenBadge";
        },
        {
            "code": 6021;
            "name": "invalidMinimumLiquidity";
        },
        {
            "code": 6022;
            "name": "invalidVestingInfo";
        },
        {
            "code": 6023;
            "name": "insufficientLiquidity";
        },
        {
            "code": 6024;
            "name": "invalidVestingAccount";
        },
        {
            "code": 6025;
            "name": "invalidPoolStatus";
        },
        {
            "code": 6026;
            "name": "unsupportNativeMintToken2022";
        },
        {
            "code": 6027;
            "name": "invalidRewardIndex";
        },
        {
            "code": 6028;
            "name": "invalidRewardDuration";
        },
        {
            "code": 6029;
            "name": "rewardInitialized";
        },
        {
            "code": 6030;
            "name": "rewardUninitialized";
        },
        {
            "code": 6031;
            "name": "invalidRewardVault";
        },
        {
            "code": 6032;
            "name": "mustWithdrawnIneligibleReward";
        },
        {
            "code": 6033;
            "name": "identicalRewardDuration";
        },
        {
            "code": 6034;
            "name": "rewardCampaignInProgress";
        },
        {
            "code": 6035;
            "name": "identicalFunder";
        },
        {
            "code": 6036;
            "name": "invalidFunder";
        },
        {
            "code": 6037;
            "name": "rewardNotEnded";
        },
        {
            "code": 6038;
            "name": "feeInverseIsIncorrect";
        },
        {
            "code": 6039;
            "name": "positionIsNotEmpty";
        },
        {
            "code": 6040;
            "name": "invalidPoolCreatorAuthority";
        },
        {
            "code": 6041;
            "name": "invalidConfigType";
        },
        {
            "code": 6042;
            "name": "invalidPoolCreator";
        },
        {
            "code": 6043;
            "name": "rewardVaultFrozenSkipRequired";
        },
        {
            "code": 6044;
            "name": "invalidSplitPositionParameters";
        },
        {
            "code": 6045;
            "name": "unsupportPositionHasVestingLock";
        },
        {
            "code": 6046;
            "name": "samePosition";
        },
        {
            "code": 6047;
            "name": "invalidBaseFeeMode";
        },
        {
            "code": 6048;
            "name": "invalidFeeRateLimiter";
        },
        {
            "code": 6049;
            "name": "failToValidateSingleSwapInstruction";
        },
        {
            "code": 6050;
            "name": "invalidFeeTimeScheduler";
        },
        {
            "code": 6051;
            "name": "undeterminedError";
        },
        {
            "code": 6052;
            "name": "invalidPoolVersion";
        },
        {
            "code": 6053;
            "name": "invalidAuthority";
        },
        {
            "code": 6054;
            "name": "invalidPermission";
        },
        {
            "code": 6055;
            "name": "invalidFeeMarketCapScheduler";
        },
        {
            "code": 6056;
            "name": "cannotUpdateBaseFee";
        },
        {
            "code": 6057;
            "name": "invalidDynamicFeeParameters";
        },
        {
            "code": 6058;
            "name": "invalidUpdatePoolFeesParameters";
        },
        {
            "code": 6059;
            "name": "missingOperatorAccount";
        },
        {
            "code": 6060;
            "name": "incorrectAta";
        },
        {
            "code": 6061;
            "name": "invalidZapOutParameters";
        },
        {
            "code": 6062;
            "name": "invalidWithdrawProtocolFeeZapAccounts";
        },
        {
            "code": 6063;
            "name": "mintRestrictedFromZap";
        },
        {
            "code": 6064;
            "name": "cpiDisabled";
        },
        {
            "code": 6065;
            "name": "missingZapOutInstruction";
        },
        {
            "code": 6066;
            "name": "invalidZapAccounts";
        },
        {
            "code": 6067;
            "name": "invalidCompoundingFeeBps";
        }
    ];
    "types": [
        {
            "name": "baseFeeParameters";
            "type": {
                "kind": "struct";
                "fields": [
                    {
                        "name": "data";
                        "type": {
                            "array": [
                                "u8",
                                27
                            ];
                        };
                    }
                ];
            };
        },
        {
            "name": "buyTokenParameters";
            "type": {
                "kind": "struct";
                "fields": [
                    {
                        "name": "copies";
                        "type": "u64";
                    }
                ];
            };
        },
        {
            "name": "claimCpAmmPoolParameters";
            "type": {
                "kind": "struct";
                "fields": [
                    {
                        "name": "amount";
                        "type": "u64";
                    }
                ];
            };
        },
        {
            "name": "config";
            "serialization": "bytemuck";
            "repr": {
                "kind": "c";
            };
            "type": {
                "kind": "struct";
                "fields": [
                    {
                        "name": "isOpen";
                        "type": "u8";
                    },
                    {
                        "name": "padding0";
                        "type": {
                            "array": [
                                "u8",
                                7
                            ];
                        };
                    },
                    {
                        "name": "quoteMint";
                        "type": "pubkey";
                    },
                    {
                        "name": "quoteVault";
                        "type": "pubkey";
                    },
                    {
                        "name": "baseTokenDecimal";
                        "type": "u8";
                    },
                    {
                        "name": "padding1";
                        "type": {
                            "array": [
                                "u8",
                                3
                            ];
                        };
                    },
                    {
                        "name": "protocolFeeBps";
                        "type": "u16";
                    },
                    {
                        "name": "padding2";
                        "type": {
                            "array": [
                                "u8",
                                2
                            ];
                        };
                    },
                    {
                        "name": "creatorFeeBps";
                        "type": "u16";
                    },
                    {
                        "name": "padding3";
                        "type": {
                            "array": [
                                "u8",
                                2
                            ];
                        };
                    },
                    {
                        "name": "prizeFeeBps";
                        "type": "u16";
                    },
                    {
                        "name": "padding4";
                        "type": {
                            "array": [
                                "u8",
                                2
                            ];
                        };
                    },
                    {
                        "name": "passThreshold";
                        "type": "u64";
                    },
                    {
                        "name": "migrationThreshold";
                        "type": "u64";
                    },
                    {
                        "name": "protocolFee";
                        "type": "u64";
                    },
                    {
                        "name": "prizePoolFee";
                        "type": "u64";
                    }
                ];
            };
        },
        {
            "name": "dynamicFeeParameters";
            "type": {
                "kind": "struct";
                "fields": [
                    {
                        "name": "binStep";
                        "type": "u16";
                    },
                    {
                        "name": "binStepU128";
                        "type": "u128";
                    },
                    {
                        "name": "filterPeriod";
                        "type": "u16";
                    },
                    {
                        "name": "decayPeriod";
                        "type": "u16";
                    },
                    {
                        "name": "reductionFactor";
                        "type": "u16";
                    },
                    {
                        "name": "maxVolatilityAccumulator";
                        "type": "u32";
                    },
                    {
                        "name": "variableFeeControl";
                        "type": "u32";
                    }
                ];
            };
        },
        {
            "name": "evtBuy";
            "type": {
                "kind": "struct";
                "fields": [
                    {
                        "name": "buyer";
                        "type": "pubkey";
                    },
                    {
                        "name": "pool";
                        "type": "pubkey";
                    },
                    {
                        "name": "baseMint";
                        "type": "pubkey";
                    },
                    {
                        "name": "quoteMint";
                        "type": "pubkey";
                    },
                    {
                        "name": "migrationBaseThreshold";
                        "type": "u64";
                    },
                    {
                        "name": "migrationThreshold";
                        "type": "u64";
                    },
                    {
                        "name": "currentTimestamp";
                        "type": "i64";
                    },
                    {
                        "name": "copies";
                        "type": "u64";
                    }
                ];
            };
        },
        {
            "name": "evtComplete";
            "type": {
                "kind": "struct";
                "fields": [
                    {
                        "name": "pool";
                        "type": "pubkey";
                    },
                    {
                        "name": "baseMint";
                        "type": "pubkey";
                    },
                    {
                        "name": "quoteMint";
                        "type": "pubkey";
                    },
                    {
                        "name": "currentTimestamp";
                        "type": "i64";
                    }
                ];
            };
        },
        {
            "name": "evtCreate";
            "type": {
                "kind": "struct";
                "fields": [
                    {
                        "name": "pool";
                        "type": "pubkey";
                    },
                    {
                        "name": "baseMint";
                        "type": "pubkey";
                    },
                    {
                        "name": "quoteMint";
                        "type": "pubkey";
                    },
                    {
                        "name": "currentTimestamp";
                        "type": "i64";
                    },
                    {
                        "name": "mintInfo";
                        "type": {
                            "defined": {
                                "name": "mintData";
                            };
                        };
                    }
                ];
            };
        },
        {
            "name": "evtIncomplete";
            "type": {
                "kind": "struct";
                "fields": [
                    {
                        "name": "pool";
                        "type": "pubkey";
                    },
                    {
                        "name": "baseMint";
                        "type": "pubkey";
                    },
                    {
                        "name": "quoteMint";
                        "type": "pubkey";
                    },
                    {
                        "name": "currentTimestamp";
                        "type": "i64";
                    }
                ];
            };
        },
        {
            "name": "evtLiquidityAdded";
            "type": {
                "kind": "struct";
                "fields": [
                    {
                        "name": "pool";
                        "type": "pubkey";
                    },
                    {
                        "name": "baseMint";
                        "type": "pubkey";
                    },
                    {
                        "name": "quoteMint";
                        "type": "pubkey";
                    },
                    {
                        "name": "currentTimestamp";
                        "type": "i64";
                    }
                ];
            };
        },
        {
            "name": "evtRefund";
            "type": {
                "kind": "struct";
                "fields": [
                    {
                        "name": "recipient";
                        "type": "pubkey";
                    },
                    {
                        "name": "pool";
                        "type": "pubkey";
                    },
                    {
                        "name": "baseMint";
                        "type": "pubkey";
                    },
                    {
                        "name": "quoteMint";
                        "type": "pubkey";
                    },
                    {
                        "name": "currentTimestamp";
                        "type": "i64";
                    }
                ];
            };
        },
        {
            "name": "initializePoolParameters";
            "type": {
                "kind": "struct";
                "fields": [
                    {
                        "name": "name";
                        "type": "string";
                    },
                    {
                        "name": "symbol";
                        "type": "string";
                    },
                    {
                        "name": "uri";
                        "type": "string";
                    }
                ];
            };
        },
        {
            "name": "migrationTokenParameters";
            "type": {
                "kind": "struct";
                "fields": [
                    {
                        "name": "baseFee";
                        "type": {
                            "defined": {
                                "name": "baseFeeParameters";
                            };
                        };
                    },
                    {
                        "name": "dynamicFee";
                        "type": {
                            "option": {
                                "defined": {
                                    "name": "dynamicFeeParameters";
                                };
                            };
                        };
                    }
                ];
            };
        },
        {
            "name": "mintData";
            "type": {
                "kind": "struct";
                "fields": [
                    {
                        "name": "creator";
                        "type": "pubkey";
                    },
                    {
                        "name": "name";
                        "type": "string";
                    },
                    {
                        "name": "symbol";
                        "type": "string";
                    },
                    {
                        "name": "uri";
                        "type": "string";
                    },
                    {
                        "name": "migrationThreshold";
                        "type": "u64";
                    }
                ];
            };
        },
        {
            "name": "poolConfig";
            "serialization": "bytemuck";
            "repr": {
                "kind": "c";
            };
            "type": {
                "kind": "struct";
                "fields": [
                    {
                        "name": "poolAuthority";
                        "type": "pubkey";
                    },
                    {
                        "name": "creator";
                        "type": "pubkey";
                    },
                    {
                        "name": "baseMint";
                        "type": "pubkey";
                    },
                    {
                        "name": "quoteMint";
                        "type": "pubkey";
                    },
                    {
                        "name": "creatorFee";
                        "type": "u64";
                    },
                    {
                        "name": "baseVault";
                        "type": "pubkey";
                    },
                    {
                        "name": "quoteVault";
                        "type": "pubkey";
                    },
                    {
                        "name": "createdAt";
                        "type": "i64";
                    },
                    {
                        "name": "migrationBaseThreshold";
                        "type": "u64";
                    },
                    {
                        "name": "migrationQuoteThreshold";
                        "type": "u64";
                    },
                    {
                        "name": "passThreshold";
                        "type": "u64";
                    },
                    {
                        "name": "liquidityAdded";
                        "type": "u8";
                    },
                    {
                        "name": "padding";
                        "type": {
                            "array": [
                                "u8",
                                7
                            ];
                        };
                    }
                ];
            };
        },
        {
            "name": "setFeeParameters";
            "type": {
                "kind": "struct";
                "fields": [
                    {
                        "name": "protocolFeeBps";
                        "type": "u16";
                    },
                    {
                        "name": "creatorFeeBps";
                        "type": "u16";
                    },
                    {
                        "name": "prizeFeeBps";
                        "type": "u16";
                    }
                ];
            };
        },
        {
            "name": "setIsOpenParameters";
            "type": {
                "kind": "struct";
                "fields": [
                    {
                        "name": "isOpen";
                        "type": "u8";
                    }
                ];
            };
        }
    ];
    "constants": [
        {
            "name": "baseVaultPrefix";
            "type": "bytes";
            "value": "[98, 97, 115, 101, 95, 118, 97, 117, 108, 116]";
        },
        {
            "name": "configPrefix";
            "type": "bytes";
            "value": "[99, 111, 110, 102, 105, 103]";
        },
        {
            "name": "poolAuthorityPrefix";
            "type": "bytes";
            "value": "[112, 111, 111, 108, 95, 97, 117, 116, 104, 111, 114, 105, 116, 121]";
        },
        {
            "name": "poolPrefix";
            "type": "bytes";
            "value": "[112, 111, 111, 108]";
        },
        {
            "name": "prizePoolVaultPrefix";
            "type": "bytes";
            "value": "[112, 114, 105, 122, 101, 95, 112, 111, 111, 108, 95, 118, 97, 117, 108, 116]";
        },
        {
            "name": "protocolVaultPrefix";
            "type": "bytes";
            "value": "[112, 114, 111, 116, 111, 99, 111, 108, 95, 102, 101, 101, 95, 118, 97, 117, 108, 116]";
        },
        {
            "name": "quoteVaultPrefix";
            "type": "bytes";
            "value": "[113, 117, 111, 116, 101, 95, 118, 97, 117, 108, 116]";
        },
        {
            "name": "userTokenAccountPrefix";
            "type": "bytes";
            "value": "[117, 115, 101, 114, 95, 116, 111, 107, 101, 110, 95, 97, 99, 99, 111, 117, 110, 116]";
        }
    ];
};

type BuyTokenAccounts = Accounts<Clawlab['instructions']['0']>['buyToken'];
type InitializePoolParameters = IdlTypes<Clawlab>['initializePoolParameters'];
type BuyTokenParameters = IdlTypes<Clawlab>['buyTokenParameters'];
type Config = IdlAccounts<Clawlab>['config'];
type PoolConfig = IdlAccounts<Clawlab>['poolConfig'];
type CreateParams = {
    payer: PublicKey;
    baseMint: PublicKey;
    name: string;
    symbol: string;
    uri: string;
};
type MintToParams = {
    payer: PublicKey;
    baseMint: PublicKey;
    copies: BN;
};
type RefundParams = {
    payer: PublicKey;
    baseMint: PublicKey;
};
type ClaimFeeParams = {
    payer: PublicKey;
    baseMint: PublicKey;
};
type ClaimTokenParams = {
    payer: PublicKey;
    baseMint: PublicKey;
};

declare class ClawlabProgram {
    program: Program<Clawlab>;
    protected connection: Connection;
    protected poolAuthority: PublicKey;
    protected eventAuthority: PublicKey;
    protected config: PublicKey;
    constructor(connection: Connection);
    protected prepareTokenAccounts(owner: PublicKey, payer: PublicKey, tokenAMint: PublicKey, tokenBMint: PublicKey, tokenAProgram: PublicKey, tokenBProgram: PublicKey): Promise<{
        ataTokenA: PublicKey;
        ataTokenB: PublicKey;
        instructions: TransactionInstruction[];
    }>;
    /**
     * Get the underlying program instance
     * @returns The program instance
     */
    getProgram(): Program<Clawlab>;
}

declare class CreatorService extends ClawlabProgram {
    private state;
    constructor(connection: Connection);
    private claimCreatorFeeIx;
    ClaimFeeIx(payer: PublicKey, baseMint: PublicKey, quoteMint: PublicKey, outputTokenAccount: PublicKey): Promise<TransactionInstruction>;
    ClaimFeeTx(params: ClaimFeeParams): Promise<Transaction>;
}

declare class PoolService extends ClawlabProgram {
    private state;
    constructor(connection: Connection);
    private initializePoolIx;
    CreateIx(payer: PublicKey, baseMint: PublicKey, quoteMint: PublicKey, params: InitializePoolParameters): Promise<TransactionInstruction>;
    CreateTx(params: CreateParams): Promise<Transaction>;
    private buyTokenIx;
    MintToIx(payer: PublicKey, baseMint: PublicKey, quoteMint: PublicKey, inputTokenAccount: PublicKey, outputTokenAccount: PublicKey, userTokenAccount: PublicKey, params: BuyTokenParameters): Promise<TransactionInstruction>;
    MintToTx(params: MintToParams): Promise<Transaction>;
    private refundTokenIx;
    RefundIx(payer: PublicKey, baseMint: PublicKey, quoteMint: PublicKey, userTokenAccount: PublicKey, outputTokenAccount: PublicKey): Promise<TransactionInstruction>;
    RefundTx(params: RefundParams): Promise<Transaction>;
}

declare class StateService extends ClawlabProgram {
    constructor(connection: Connection);
    getConfig(): Promise<Config>;
    getPoolConfig(poolAddress: PublicKey | string): Promise<PoolConfig>;
}

declare class UserService extends ClawlabProgram {
    private state;
    constructor(connection: Connection);
    private claimUserTokenIx;
    ClaimTokenIx(payer: PublicKey, baseMint: PublicKey, quoteMint: PublicKey, inputTokenAccount: PublicKey, outputTokenAccount: PublicKey): Promise<TransactionInstruction>;
    ClaimTokenTx(params: ClaimTokenParams): Promise<Transaction>;
}

declare class ClawlabClient {
    state: StateService;
    user: UserService;
    creator: CreatorService;
    pool: PoolService;
    connection: Connection;
    constructor(connection: Connection);
    static create(connection: Connection, commitment?: Commitment): ClawlabClient;
}

declare const CLAWLAB_PROGRAM_ID: PublicKey;
declare const DAMM_V2_PROGRAM_ID: PublicKey;
declare const METAPLEX_PROGRAM_ID: PublicKey;

/**
 * Generic account fetch helper
 * @param accountAddress - The address of the account to fetch
 * @param accountType - The type of account to fetch from program.account
 * @param program - The program instance
 * @param commitment - The commitment level
 * @returns The fetched account data
 */
declare function getAccountData<T>(accountAddress: PublicKey | string, accountType: keyof Program<Clawlab>['account'], program: Program<Clawlab>, commitment: Commitment | undefined): Promise<T>;
/**
 * Get creation timestamp for an account
 * @param accountAddress - The address of the account
 * @param connection - The Solana connection instance
 * @returns The creation timestamp as a Date object, or undefined if not found
 */
declare function getAccountCreationTimestamp(accountAddress: PublicKey | string, connection: Connection): Promise<Date | undefined>;
/**
 * Get creation timestamps for multiple accounts
 * @param accountAddresses - Array of account addresses
 * @param connection - The Solana connection instance
 * @returns Array of creation timestamps corresponding to the input addresses
 */
declare function getAccountCreationTimestamps(accountAddresses: (PublicKey | string)[], connection: Connection): Promise<(Date | undefined)[]>;
/**
 * Get the total token supply
 * @param swapBaseAmount - The swap base amount
 * @param migrationBaseThreshold - The migration base threshold
 * @param lockedVestingParams - The locked vesting parameters
 * @returns The total token supply
 */
declare function getTotalTokenSupply(swapBaseAmount: BN$1, migrationBaseThreshold: BN$1, lockedVestingParams: {
    amountPerPeriod: BN$1;
    numberOfPeriod: BN$1;
    cliffUnlockAmount: BN$1;
}): BN$1;

/**
 * Program IDL in camelCase format in order to be used in JS/TS.
 *
 * Note that this is only a type helper and is not the actual IDL. The original
 * IDL can be found at `target/idl/cp_amm.json`.
 */
type CpAmm = {
    address: 'cpamdpZCGKUy5JxQXB4dcpGPiikHawvSWAd6mEn1sGG';
    metadata: {
        name: 'cpAmm';
        version: '0.1.7';
        spec: '0.1.0';
        description: 'Created with Anchor';
    };
    instructions: [
        {
            name: 'addLiquidity';
            discriminator: [181, 157, 89, 67, 143, 182, 52, 72];
            accounts: [
                {
                    name: 'pool';
                    writable: true;
                    relations: ['position'];
                },
                {
                    name: 'position';
                    writable: true;
                },
                {
                    name: 'tokenAAccount';
                    docs: ['The user token a account'];
                    writable: true;
                },
                {
                    name: 'tokenBAccount';
                    docs: ['The user token b account'];
                    writable: true;
                },
                {
                    name: 'tokenAVault';
                    docs: ['The vault token account for input token'];
                    writable: true;
                    relations: ['pool'];
                },
                {
                    name: 'tokenBVault';
                    docs: ['The vault token account for output token'];
                    writable: true;
                    relations: ['pool'];
                },
                {
                    name: 'tokenAMint';
                    docs: ['The mint of token a'];
                    relations: ['pool'];
                },
                {
                    name: 'tokenBMint';
                    docs: ['The mint of token b'];
                    relations: ['pool'];
                },
                {
                    name: 'positionNftAccount';
                    docs: ['The token account for nft'];
                },
                {
                    name: 'owner';
                    docs: ['owner of position'];
                    signer: true;
                },
                {
                    name: 'tokenAProgram';
                    docs: ['Token a program'];
                },
                {
                    name: 'tokenBProgram';
                    docs: ['Token b program'];
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'params';
                    type: {
                        defined: {
                            name: 'addLiquidityParameters';
                        };
                    };
                }
            ];
        },
        {
            name: 'claimPartnerFee';
            discriminator: [97, 206, 39, 105, 94, 94, 126, 148];
            accounts: [
                {
                    name: 'poolAuthority';
                    address: 'HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC';
                },
                {
                    name: 'pool';
                    writable: true;
                },
                {
                    name: 'tokenAAccount';
                    docs: ['The treasury token a account'];
                    writable: true;
                },
                {
                    name: 'tokenBAccount';
                    docs: ['The treasury token b account'];
                    writable: true;
                },
                {
                    name: 'tokenAVault';
                    docs: ['The vault token account for input token'];
                    writable: true;
                    relations: ['pool'];
                },
                {
                    name: 'tokenBVault';
                    docs: ['The vault token account for output token'];
                    writable: true;
                    relations: ['pool'];
                },
                {
                    name: 'tokenAMint';
                    docs: ['The mint of token a'];
                    relations: ['pool'];
                },
                {
                    name: 'tokenBMint';
                    docs: ['The mint of token b'];
                    relations: ['pool'];
                },
                {
                    name: 'partner';
                    signer: true;
                    relations: ['pool'];
                },
                {
                    name: 'tokenAProgram';
                    docs: ['Token a program'];
                },
                {
                    name: 'tokenBProgram';
                    docs: ['Token b program'];
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'maxAmountA';
                    type: 'u64';
                },
                {
                    name: 'maxAmountB';
                    type: 'u64';
                }
            ];
        },
        {
            name: 'claimPositionFee';
            discriminator: [180, 38, 154, 17, 133, 33, 162, 211];
            accounts: [
                {
                    name: 'poolAuthority';
                    address: 'HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC';
                },
                {
                    name: 'pool';
                    relations: ['position'];
                },
                {
                    name: 'position';
                    writable: true;
                },
                {
                    name: 'tokenAAccount';
                    docs: ['The user token a account'];
                    writable: true;
                },
                {
                    name: 'tokenBAccount';
                    docs: ['The user token b account'];
                    writable: true;
                },
                {
                    name: 'tokenAVault';
                    docs: ['The vault token account for input token'];
                    writable: true;
                    relations: ['pool'];
                },
                {
                    name: 'tokenBVault';
                    docs: ['The vault token account for output token'];
                    writable: true;
                    relations: ['pool'];
                },
                {
                    name: 'tokenAMint';
                    docs: ['The mint of token a'];
                    relations: ['pool'];
                },
                {
                    name: 'tokenBMint';
                    docs: ['The mint of token b'];
                    relations: ['pool'];
                },
                {
                    name: 'positionNftAccount';
                    docs: ['The token account for nft'];
                },
                {
                    name: 'owner';
                    docs: ['owner of position'];
                    signer: true;
                },
                {
                    name: 'tokenAProgram';
                    docs: ['Token a program'];
                },
                {
                    name: 'tokenBProgram';
                    docs: ['Token b program'];
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [];
        },
        {
            name: 'claimProtocolFee';
            discriminator: [165, 228, 133, 48, 99, 249, 255, 33];
            accounts: [
                {
                    name: 'poolAuthority';
                    address: 'HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC';
                },
                {
                    name: 'pool';
                    writable: true;
                },
                {
                    name: 'tokenAVault';
                    docs: ['The vault token account for input token'];
                    writable: true;
                    relations: ['pool'];
                },
                {
                    name: 'tokenBVault';
                    docs: ['The vault token account for output token'];
                    writable: true;
                    relations: ['pool'];
                },
                {
                    name: 'tokenAMint';
                    docs: ['The mint of token a'];
                    relations: ['pool'];
                },
                {
                    name: 'tokenBMint';
                    docs: ['The mint of token b'];
                    relations: ['pool'];
                },
                {
                    name: 'tokenAAccount';
                    writable: true;
                },
                {
                    name: 'tokenBAccount';
                    writable: true;
                },
                {
                    name: 'operator';
                    docs: ['Claim fee operator'];
                },
                {
                    name: 'signer';
                    docs: ['operator'];
                    signer: true;
                },
                {
                    name: 'tokenAProgram';
                    docs: ['Token a program'];
                },
                {
                    name: 'tokenBProgram';
                    docs: ['Token b program'];
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'maxAmountA';
                    type: 'u64';
                },
                {
                    name: 'maxAmountB';
                    type: 'u64';
                }
            ];
        },
        {
            name: 'claimReward';
            discriminator: [149, 95, 181, 242, 94, 90, 158, 162];
            accounts: [
                {
                    name: 'poolAuthority';
                    address: 'HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC';
                },
                {
                    name: 'pool';
                    writable: true;
                    relations: ['position'];
                },
                {
                    name: 'position';
                    writable: true;
                },
                {
                    name: 'rewardVault';
                    docs: ['The vault token account for reward token'];
                    writable: true;
                },
                {
                    name: 'rewardMint';
                },
                {
                    name: 'userTokenAccount';
                    writable: true;
                },
                {
                    name: 'positionNftAccount';
                    docs: ['The token account for nft'];
                },
                {
                    name: 'owner';
                    docs: ['owner of position'];
                    signer: true;
                },
                {
                    name: 'tokenProgram';
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'rewardIndex';
                    type: 'u8';
                },
                {
                    name: 'skipReward';
                    type: 'u8';
                }
            ];
        },
        {
            name: 'closeConfig';
            discriminator: [145, 9, 72, 157, 95, 125, 61, 85];
            accounts: [
                {
                    name: 'config';
                    writable: true;
                },
                {
                    name: 'operator';
                },
                {
                    name: 'signer';
                    signer: true;
                },
                {
                    name: 'rentReceiver';
                    writable: true;
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [];
        },
        {
            name: 'closeOperatorAccount';
            discriminator: [171, 9, 213, 74, 120, 23, 3, 29];
            accounts: [
                {
                    name: 'operator';
                    writable: true;
                },
                {
                    name: 'signer';
                    signer: true;
                },
                {
                    name: 'rentReceiver';
                    writable: true;
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [];
        },
        {
            name: 'closePosition';
            discriminator: [123, 134, 81, 0, 49, 68, 98, 98];
            accounts: [
                {
                    name: 'positionNftMint';
                    docs: ['positionNftMint'];
                    writable: true;
                },
                {
                    name: 'positionNftAccount';
                    docs: ['The token account for nft'];
                    writable: true;
                },
                {
                    name: 'pool';
                    writable: true;
                    relations: ['position'];
                },
                {
                    name: 'position';
                    writable: true;
                },
                {
                    name: 'poolAuthority';
                    address: 'HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC';
                },
                {
                    name: 'rentReceiver';
                    writable: true;
                },
                {
                    name: 'owner';
                    docs: ['Owner of position'];
                    signer: true;
                },
                {
                    name: 'tokenProgram';
                    docs: [
                        'Program to create NFT mint/token account and transfer for token22 account'
                    ];
                    address: 'TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb';
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [];
        },
        {
            name: 'closeTokenBadge';
            discriminator: [108, 146, 86, 110, 179, 254, 10, 104];
            accounts: [
                {
                    name: 'tokenBadge';
                    writable: true;
                },
                {
                    name: 'operator';
                },
                {
                    name: 'signer';
                    signer: true;
                },
                {
                    name: 'rentReceiver';
                    writable: true;
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [];
        },
        {
            name: 'createConfig';
            docs: ['OPERATOR FUNCTIONS /////'];
            discriminator: [201, 207, 243, 114, 75, 111, 47, 189];
            accounts: [
                {
                    name: 'config';
                    writable: true;
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [99, 111, 110, 102, 105, 103];
                            },
                            {
                                kind: 'arg';
                                path: 'index';
                            }
                        ];
                    };
                },
                {
                    name: 'operator';
                },
                {
                    name: 'signer';
                    signer: true;
                },
                {
                    name: 'payer';
                    writable: true;
                    signer: true;
                },
                {
                    name: 'systemProgram';
                    address: '11111111111111111111111111111111';
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'index';
                    type: 'u64';
                },
                {
                    name: 'configParameters';
                    type: {
                        defined: {
                            name: 'staticConfigParameters';
                        };
                    };
                }
            ];
        },
        {
            name: 'createDynamicConfig';
            discriminator: [81, 251, 122, 78, 66, 57, 208, 82];
            accounts: [
                {
                    name: 'config';
                    writable: true;
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [99, 111, 110, 102, 105, 103];
                            },
                            {
                                kind: 'arg';
                                path: 'index';
                            }
                        ];
                    };
                },
                {
                    name: 'operator';
                },
                {
                    name: 'signer';
                    signer: true;
                },
                {
                    name: 'payer';
                    writable: true;
                    signer: true;
                },
                {
                    name: 'systemProgram';
                    address: '11111111111111111111111111111111';
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'index';
                    type: 'u64';
                },
                {
                    name: 'configParameters';
                    type: {
                        defined: {
                            name: 'dynamicConfigParameters';
                        };
                    };
                }
            ];
        },
        {
            name: 'createOperatorAccount';
            docs: ['ADMIN FUNCTIONS /////'];
            discriminator: [221, 64, 246, 149, 240, 153, 229, 163];
            accounts: [
                {
                    name: 'operator';
                    writable: true;
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [111, 112, 101, 114, 97, 116, 111, 114];
                            },
                            {
                                kind: 'account';
                                path: 'whitelistedAddress';
                            }
                        ];
                    };
                },
                {
                    name: 'whitelistedAddress';
                },
                {
                    name: 'signer';
                    signer: true;
                },
                {
                    name: 'payer';
                    writable: true;
                    signer: true;
                },
                {
                    name: 'systemProgram';
                    address: '11111111111111111111111111111111';
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'permission';
                    type: 'u128';
                }
            ];
        },
        {
            name: 'createPosition';
            discriminator: [48, 215, 197, 153, 96, 203, 180, 133];
            accounts: [
                {
                    name: 'owner';
                },
                {
                    name: 'positionNftMint';
                    docs: ['positionNftMint'];
                    writable: true;
                    signer: true;
                },
                {
                    name: 'positionNftAccount';
                    docs: ['position nft account'];
                    writable: true;
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    112,
                                    111,
                                    115,
                                    105,
                                    116,
                                    105,
                                    111,
                                    110,
                                    95,
                                    110,
                                    102,
                                    116,
                                    95,
                                    97,
                                    99,
                                    99,
                                    111,
                                    117,
                                    110,
                                    116
                                ];
                            },
                            {
                                kind: 'account';
                                path: 'positionNftMint';
                            }
                        ];
                    };
                },
                {
                    name: 'pool';
                    writable: true;
                },
                {
                    name: 'position';
                    writable: true;
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [112, 111, 115, 105, 116, 105, 111, 110];
                            },
                            {
                                kind: 'account';
                                path: 'positionNftMint';
                            }
                        ];
                    };
                },
                {
                    name: 'poolAuthority';
                    address: 'HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC';
                },
                {
                    name: 'payer';
                    docs: [
                        'Address paying to create the position. Can be anyone'
                    ];
                    writable: true;
                    signer: true;
                },
                {
                    name: 'tokenProgram';
                    docs: [
                        'Program to create NFT mint/token account and transfer for token22 account'
                    ];
                    address: 'TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb';
                },
                {
                    name: 'systemProgram';
                    address: '11111111111111111111111111111111';
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [];
        },
        {
            name: 'createTokenBadge';
            discriminator: [88, 206, 0, 91, 60, 175, 151, 118];
            accounts: [
                {
                    name: 'tokenBadge';
                    writable: true;
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    116,
                                    111,
                                    107,
                                    101,
                                    110,
                                    95,
                                    98,
                                    97,
                                    100,
                                    103,
                                    101
                                ];
                            },
                            {
                                kind: 'account';
                                path: 'tokenMint';
                            }
                        ];
                    };
                },
                {
                    name: 'tokenMint';
                },
                {
                    name: 'operator';
                },
                {
                    name: 'signer';
                    signer: true;
                },
                {
                    name: 'payer';
                    writable: true;
                    signer: true;
                },
                {
                    name: 'systemProgram';
                    address: '11111111111111111111111111111111';
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [];
        },
        {
            name: 'dummyIx';
            discriminator: [234, 95, 176, 185, 7, 42, 35, 159];
            accounts: [
                {
                    name: 'podAlignedFeeTimeScheduler';
                },
                {
                    name: 'podAlignedFeeRateLimiter';
                },
                {
                    name: 'podAlignedFeeMarketCapScheduler';
                }
            ];
            args: [
                {
                    name: 'ixs';
                    type: {
                        defined: {
                            name: 'dummyParams';
                        };
                    };
                }
            ];
        },
        {
            name: 'fundReward';
            discriminator: [188, 50, 249, 165, 93, 151, 38, 63];
            accounts: [
                {
                    name: 'pool';
                    writable: true;
                },
                {
                    name: 'rewardVault';
                    writable: true;
                },
                {
                    name: 'rewardMint';
                },
                {
                    name: 'funderTokenAccount';
                    writable: true;
                },
                {
                    name: 'funder';
                    signer: true;
                },
                {
                    name: 'tokenProgram';
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'rewardIndex';
                    type: 'u8';
                },
                {
                    name: 'amount';
                    type: 'u64';
                },
                {
                    name: 'carryForward';
                    type: 'bool';
                }
            ];
        },
        {
            name: 'initializeCustomizablePool';
            discriminator: [20, 161, 241, 24, 189, 221, 180, 2];
            accounts: [
                {
                    name: 'creator';
                },
                {
                    name: 'positionNftMint';
                    docs: ['positionNftMint'];
                    writable: true;
                    signer: true;
                },
                {
                    name: 'positionNftAccount';
                    docs: ['position nft account'];
                    writable: true;
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    112,
                                    111,
                                    115,
                                    105,
                                    116,
                                    105,
                                    111,
                                    110,
                                    95,
                                    110,
                                    102,
                                    116,
                                    95,
                                    97,
                                    99,
                                    99,
                                    111,
                                    117,
                                    110,
                                    116
                                ];
                            },
                            {
                                kind: 'account';
                                path: 'positionNftMint';
                            }
                        ];
                    };
                },
                {
                    name: 'payer';
                    docs: ['Address paying to create the pool. Can be anyone'];
                    writable: true;
                    signer: true;
                },
                {
                    name: 'poolAuthority';
                    address: 'HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC';
                },
                {
                    name: 'pool';
                    docs: ['Initialize an account to store the pool state'];
                    writable: true;
                },
                {
                    name: 'position';
                    writable: true;
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [112, 111, 115, 105, 116, 105, 111, 110];
                            },
                            {
                                kind: 'account';
                                path: 'positionNftMint';
                            }
                        ];
                    };
                },
                {
                    name: 'tokenAMint';
                    docs: ['Token a mint'];
                },
                {
                    name: 'tokenBMint';
                    docs: ['Token b mint'];
                },
                {
                    name: 'tokenAVault';
                    docs: ['Token a vault for the pool'];
                    writable: true;
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    116,
                                    111,
                                    107,
                                    101,
                                    110,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                kind: 'account';
                                path: 'tokenAMint';
                            },
                            {
                                kind: 'account';
                                path: 'pool';
                            }
                        ];
                    };
                },
                {
                    name: 'tokenBVault';
                    docs: ['Token b vault for the pool'];
                    writable: true;
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    116,
                                    111,
                                    107,
                                    101,
                                    110,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                kind: 'account';
                                path: 'tokenBMint';
                            },
                            {
                                kind: 'account';
                                path: 'pool';
                            }
                        ];
                    };
                },
                {
                    name: 'payerTokenA';
                    docs: ['payer token a account'];
                    writable: true;
                },
                {
                    name: 'payerTokenB';
                    docs: ['creator token b account'];
                    writable: true;
                },
                {
                    name: 'tokenAProgram';
                    docs: ['Program to create mint account and mint tokens'];
                },
                {
                    name: 'tokenBProgram';
                    docs: ['Program to create mint account and mint tokens'];
                },
                {
                    name: 'token2022Program';
                    docs: [
                        'Program to create NFT mint/token account and transfer for token22 account'
                    ];
                    address: 'TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb';
                },
                {
                    name: 'systemProgram';
                    address: '11111111111111111111111111111111';
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'params';
                    type: {
                        defined: {
                            name: 'initializeCustomizablePoolParameters';
                        };
                    };
                }
            ];
        },
        {
            name: 'initializePool';
            docs: ['USER FUNCTIONS ////'];
            discriminator: [95, 180, 10, 172, 84, 174, 232, 40];
            accounts: [
                {
                    name: 'creator';
                },
                {
                    name: 'positionNftMint';
                    docs: ['positionNftMint'];
                    writable: true;
                    signer: true;
                },
                {
                    name: 'positionNftAccount';
                    docs: ['position nft account'];
                    writable: true;
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    112,
                                    111,
                                    115,
                                    105,
                                    116,
                                    105,
                                    111,
                                    110,
                                    95,
                                    110,
                                    102,
                                    116,
                                    95,
                                    97,
                                    99,
                                    99,
                                    111,
                                    117,
                                    110,
                                    116
                                ];
                            },
                            {
                                kind: 'account';
                                path: 'positionNftMint';
                            }
                        ];
                    };
                },
                {
                    name: 'payer';
                    docs: ['Address paying to create the pool. Can be anyone'];
                    writable: true;
                    signer: true;
                },
                {
                    name: 'config';
                    docs: ['Which config the pool belongs to.'];
                },
                {
                    name: 'poolAuthority';
                    address: 'HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC';
                },
                {
                    name: 'pool';
                    docs: ['Initialize an account to store the pool state'];
                    writable: true;
                },
                {
                    name: 'position';
                    writable: true;
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [112, 111, 115, 105, 116, 105, 111, 110];
                            },
                            {
                                kind: 'account';
                                path: 'positionNftMint';
                            }
                        ];
                    };
                },
                {
                    name: 'tokenAMint';
                    docs: ['Token a mint'];
                },
                {
                    name: 'tokenBMint';
                    docs: ['Token b mint'];
                },
                {
                    name: 'tokenAVault';
                    docs: ['Token a vault for the pool'];
                    writable: true;
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    116,
                                    111,
                                    107,
                                    101,
                                    110,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                kind: 'account';
                                path: 'tokenAMint';
                            },
                            {
                                kind: 'account';
                                path: 'pool';
                            }
                        ];
                    };
                },
                {
                    name: 'tokenBVault';
                    docs: ['Token b vault for the pool'];
                    writable: true;
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    116,
                                    111,
                                    107,
                                    101,
                                    110,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                kind: 'account';
                                path: 'tokenBMint';
                            },
                            {
                                kind: 'account';
                                path: 'pool';
                            }
                        ];
                    };
                },
                {
                    name: 'payerTokenA';
                    docs: ['payer token a account'];
                    writable: true;
                },
                {
                    name: 'payerTokenB';
                    docs: ['creator token b account'];
                    writable: true;
                },
                {
                    name: 'tokenAProgram';
                    docs: ['Program to create mint account and mint tokens'];
                },
                {
                    name: 'tokenBProgram';
                    docs: ['Program to create mint account and mint tokens'];
                },
                {
                    name: 'token2022Program';
                    docs: [
                        'Program to create NFT mint/token account and transfer for token22 account'
                    ];
                    address: 'TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb';
                },
                {
                    name: 'systemProgram';
                    address: '11111111111111111111111111111111';
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'params';
                    type: {
                        defined: {
                            name: 'initializePoolParameters';
                        };
                    };
                }
            ];
        },
        {
            name: 'initializePoolWithDynamicConfig';
            discriminator: [149, 82, 72, 197, 253, 252, 68, 15];
            accounts: [
                {
                    name: 'creator';
                },
                {
                    name: 'positionNftMint';
                    docs: ['positionNftMint'];
                    writable: true;
                    signer: true;
                },
                {
                    name: 'positionNftAccount';
                    docs: ['position nft account'];
                    writable: true;
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    112,
                                    111,
                                    115,
                                    105,
                                    116,
                                    105,
                                    111,
                                    110,
                                    95,
                                    110,
                                    102,
                                    116,
                                    95,
                                    97,
                                    99,
                                    99,
                                    111,
                                    117,
                                    110,
                                    116
                                ];
                            },
                            {
                                kind: 'account';
                                path: 'positionNftMint';
                            }
                        ];
                    };
                },
                {
                    name: 'payer';
                    docs: ['Address paying to create the pool. Can be anyone'];
                    writable: true;
                    signer: true;
                },
                {
                    name: 'poolCreatorAuthority';
                    signer: true;
                    relations: ['config'];
                },
                {
                    name: 'config';
                    docs: ['Which config the pool belongs to.'];
                },
                {
                    name: 'poolAuthority';
                    address: 'HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC';
                },
                {
                    name: 'pool';
                    docs: ['Initialize an account to store the pool state'];
                    writable: true;
                },
                {
                    name: 'position';
                    writable: true;
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [112, 111, 115, 105, 116, 105, 111, 110];
                            },
                            {
                                kind: 'account';
                                path: 'positionNftMint';
                            }
                        ];
                    };
                },
                {
                    name: 'tokenAMint';
                    docs: ['Token a mint'];
                },
                {
                    name: 'tokenBMint';
                    docs: ['Token b mint'];
                },
                {
                    name: 'tokenAVault';
                    docs: ['Token a vault for the pool'];
                    writable: true;
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    116,
                                    111,
                                    107,
                                    101,
                                    110,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                kind: 'account';
                                path: 'tokenAMint';
                            },
                            {
                                kind: 'account';
                                path: 'pool';
                            }
                        ];
                    };
                },
                {
                    name: 'tokenBVault';
                    docs: ['Token b vault for the pool'];
                    writable: true;
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    116,
                                    111,
                                    107,
                                    101,
                                    110,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                kind: 'account';
                                path: 'tokenBMint';
                            },
                            {
                                kind: 'account';
                                path: 'pool';
                            }
                        ];
                    };
                },
                {
                    name: 'payerTokenA';
                    docs: ['payer token a account'];
                    writable: true;
                },
                {
                    name: 'payerTokenB';
                    docs: ['creator token b account'];
                    writable: true;
                },
                {
                    name: 'tokenAProgram';
                    docs: ['Program to create mint account and mint tokens'];
                },
                {
                    name: 'tokenBProgram';
                    docs: ['Program to create mint account and mint tokens'];
                },
                {
                    name: 'token2022Program';
                    docs: [
                        'Program to create NFT mint/token account and transfer for token22 account'
                    ];
                    address: 'TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb';
                },
                {
                    name: 'systemProgram';
                    address: '11111111111111111111111111111111';
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'params';
                    type: {
                        defined: {
                            name: 'initializeCustomizablePoolParameters';
                        };
                    };
                }
            ];
        },
        {
            name: 'initializeReward';
            discriminator: [95, 135, 192, 196, 242, 129, 230, 68];
            accounts: [
                {
                    name: 'poolAuthority';
                    address: 'HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC';
                },
                {
                    name: 'pool';
                    writable: true;
                },
                {
                    name: 'rewardVault';
                    writable: true;
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    114,
                                    101,
                                    119,
                                    97,
                                    114,
                                    100,
                                    95,
                                    118,
                                    97,
                                    117,
                                    108,
                                    116
                                ];
                            },
                            {
                                kind: 'account';
                                path: 'pool';
                            },
                            {
                                kind: 'arg';
                                path: 'rewardIndex';
                            }
                        ];
                    };
                },
                {
                    name: 'rewardMint';
                },
                {
                    name: 'signer';
                    signer: true;
                },
                {
                    name: 'payer';
                    writable: true;
                    signer: true;
                },
                {
                    name: 'tokenProgram';
                },
                {
                    name: 'systemProgram';
                    address: '11111111111111111111111111111111';
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'rewardIndex';
                    type: 'u8';
                },
                {
                    name: 'rewardDuration';
                    type: 'u64';
                },
                {
                    name: 'funder';
                    type: 'pubkey';
                }
            ];
        },
        {
            name: 'lockPosition';
            discriminator: [227, 62, 2, 252, 247, 10, 171, 185];
            accounts: [
                {
                    name: 'pool';
                    relations: ['position'];
                },
                {
                    name: 'position';
                    writable: true;
                },
                {
                    name: 'vesting';
                    writable: true;
                    signer: true;
                },
                {
                    name: 'positionNftAccount';
                    docs: ['The token account for nft'];
                },
                {
                    name: 'owner';
                    docs: ['owner of position'];
                    signer: true;
                },
                {
                    name: 'payer';
                    writable: true;
                    signer: true;
                },
                {
                    name: 'systemProgram';
                    address: '11111111111111111111111111111111';
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'params';
                    type: {
                        defined: {
                            name: 'vestingParameters';
                        };
                    };
                }
            ];
        },
        {
            name: 'permanentLockPosition';
            discriminator: [165, 176, 125, 6, 231, 171, 186, 213];
            accounts: [
                {
                    name: 'pool';
                    writable: true;
                    relations: ['position'];
                },
                {
                    name: 'position';
                    writable: true;
                },
                {
                    name: 'positionNftAccount';
                    docs: ['The token account for nft'];
                },
                {
                    name: 'owner';
                    docs: ['owner of position'];
                    signer: true;
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'permanentLockLiquidity';
                    type: 'u128';
                }
            ];
        },
        {
            name: 'refreshVesting';
            discriminator: [9, 94, 216, 14, 116, 204, 247, 0];
            accounts: [
                {
                    name: 'pool';
                    relations: ['position'];
                },
                {
                    name: 'position';
                    writable: true;
                },
                {
                    name: 'positionNftAccount';
                    docs: ['The token account for nft'];
                },
                {
                    name: 'owner';
                }
            ];
            args: [];
        },
        {
            name: 'removeAllLiquidity';
            discriminator: [10, 51, 61, 35, 112, 105, 24, 85];
            accounts: [
                {
                    name: 'poolAuthority';
                    address: 'HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC';
                },
                {
                    name: 'pool';
                    writable: true;
                    relations: ['position'];
                },
                {
                    name: 'position';
                    writable: true;
                },
                {
                    name: 'tokenAAccount';
                    docs: ['The user token a account'];
                    writable: true;
                },
                {
                    name: 'tokenBAccount';
                    docs: ['The user token b account'];
                    writable: true;
                },
                {
                    name: 'tokenAVault';
                    docs: ['The vault token account for input token'];
                    writable: true;
                    relations: ['pool'];
                },
                {
                    name: 'tokenBVault';
                    docs: ['The vault token account for output token'];
                    writable: true;
                    relations: ['pool'];
                },
                {
                    name: 'tokenAMint';
                    docs: ['The mint of token a'];
                    relations: ['pool'];
                },
                {
                    name: 'tokenBMint';
                    docs: ['The mint of token b'];
                    relations: ['pool'];
                },
                {
                    name: 'positionNftAccount';
                    docs: ['The token account for nft'];
                },
                {
                    name: 'owner';
                    docs: ['owner of position'];
                    signer: true;
                },
                {
                    name: 'tokenAProgram';
                    docs: ['Token a program'];
                },
                {
                    name: 'tokenBProgram';
                    docs: ['Token b program'];
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'tokenAAmountThreshold';
                    type: 'u64';
                },
                {
                    name: 'tokenBAmountThreshold';
                    type: 'u64';
                }
            ];
        },
        {
            name: 'removeLiquidity';
            discriminator: [80, 85, 209, 72, 24, 206, 177, 108];
            accounts: [
                {
                    name: 'poolAuthority';
                    address: 'HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC';
                },
                {
                    name: 'pool';
                    writable: true;
                    relations: ['position'];
                },
                {
                    name: 'position';
                    writable: true;
                },
                {
                    name: 'tokenAAccount';
                    docs: ['The user token a account'];
                    writable: true;
                },
                {
                    name: 'tokenBAccount';
                    docs: ['The user token b account'];
                    writable: true;
                },
                {
                    name: 'tokenAVault';
                    docs: ['The vault token account for input token'];
                    writable: true;
                    relations: ['pool'];
                },
                {
                    name: 'tokenBVault';
                    docs: ['The vault token account for output token'];
                    writable: true;
                    relations: ['pool'];
                },
                {
                    name: 'tokenAMint';
                    docs: ['The mint of token a'];
                    relations: ['pool'];
                },
                {
                    name: 'tokenBMint';
                    docs: ['The mint of token b'];
                    relations: ['pool'];
                },
                {
                    name: 'positionNftAccount';
                    docs: ['The token account for nft'];
                },
                {
                    name: 'owner';
                    docs: ['owner of position'];
                    signer: true;
                },
                {
                    name: 'tokenAProgram';
                    docs: ['Token a program'];
                },
                {
                    name: 'tokenBProgram';
                    docs: ['Token b program'];
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'params';
                    type: {
                        defined: {
                            name: 'removeLiquidityParameters';
                        };
                    };
                }
            ];
        },
        {
            name: 'setPoolStatus';
            discriminator: [112, 87, 135, 223, 83, 204, 132, 53];
            accounts: [
                {
                    name: 'pool';
                    writable: true;
                },
                {
                    name: 'operator';
                },
                {
                    name: 'signer';
                    signer: true;
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'status';
                    type: 'u8';
                }
            ];
        },
        {
            name: 'splitPosition';
            discriminator: [172, 241, 221, 138, 161, 29, 253, 42];
            accounts: [
                {
                    name: 'pool';
                    writable: true;
                    relations: ['firstPosition', 'secondPosition'];
                },
                {
                    name: 'firstPosition';
                    docs: ['The first position'];
                    writable: true;
                },
                {
                    name: 'firstPositionNftAccount';
                    docs: ['The token account for position nft'];
                },
                {
                    name: 'secondPosition';
                    docs: ['The second position'];
                    writable: true;
                },
                {
                    name: 'secondPositionNftAccount';
                    docs: ['The token account for position nft'];
                },
                {
                    name: 'firstOwner';
                    docs: ['Owner of first position'];
                    signer: true;
                },
                {
                    name: 'secondOwner';
                    docs: ['Owner of second position'];
                    signer: true;
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'params';
                    type: {
                        defined: {
                            name: 'splitPositionParameters';
                        };
                    };
                }
            ];
        },
        {
            name: 'splitPosition2';
            discriminator: [221, 147, 228, 207, 140, 212, 17, 119];
            accounts: [
                {
                    name: 'pool';
                    writable: true;
                    relations: ['firstPosition', 'secondPosition'];
                },
                {
                    name: 'firstPosition';
                    docs: ['The first position'];
                    writable: true;
                },
                {
                    name: 'firstPositionNftAccount';
                    docs: ['The token account for position nft'];
                },
                {
                    name: 'secondPosition';
                    docs: ['The second position'];
                    writable: true;
                },
                {
                    name: 'secondPositionNftAccount';
                    docs: ['The token account for position nft'];
                },
                {
                    name: 'firstOwner';
                    docs: ['Owner of first position'];
                    signer: true;
                },
                {
                    name: 'secondOwner';
                    docs: ['Owner of second position'];
                    signer: true;
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'numerator';
                    type: 'u32';
                }
            ];
        },
        {
            name: 'swap';
            discriminator: [248, 198, 158, 145, 225, 117, 135, 200];
            accounts: [
                {
                    name: 'poolAuthority';
                    address: 'HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC';
                },
                {
                    name: 'pool';
                    docs: ['Pool account'];
                    writable: true;
                },
                {
                    name: 'inputTokenAccount';
                    docs: ['The user token account for input token'];
                    writable: true;
                },
                {
                    name: 'outputTokenAccount';
                    docs: ['The user token account for output token'];
                    writable: true;
                },
                {
                    name: 'tokenAVault';
                    docs: ['The vault token account for input token'];
                    writable: true;
                    relations: ['pool'];
                },
                {
                    name: 'tokenBVault';
                    docs: ['The vault token account for output token'];
                    writable: true;
                    relations: ['pool'];
                },
                {
                    name: 'tokenAMint';
                    docs: ['The mint of token a'];
                },
                {
                    name: 'tokenBMint';
                    docs: ['The mint of token b'];
                },
                {
                    name: 'payer';
                    docs: ['The user performing the swap'];
                    signer: true;
                },
                {
                    name: 'tokenAProgram';
                    docs: ['Token a program'];
                },
                {
                    name: 'tokenBProgram';
                    docs: ['Token b program'];
                },
                {
                    name: 'referralTokenAccount';
                    docs: ['referral token account'];
                    writable: true;
                    optional: true;
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'params';
                    type: {
                        defined: {
                            name: 'swapParameters';
                        };
                    };
                }
            ];
        },
        {
            name: 'swap2';
            discriminator: [65, 75, 63, 76, 235, 91, 91, 136];
            accounts: [
                {
                    name: 'poolAuthority';
                    address: 'HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC';
                },
                {
                    name: 'pool';
                    docs: ['Pool account'];
                    writable: true;
                },
                {
                    name: 'inputTokenAccount';
                    docs: ['The user token account for input token'];
                    writable: true;
                },
                {
                    name: 'outputTokenAccount';
                    docs: ['The user token account for output token'];
                    writable: true;
                },
                {
                    name: 'tokenAVault';
                    docs: ['The vault token account for input token'];
                    writable: true;
                    relations: ['pool'];
                },
                {
                    name: 'tokenBVault';
                    docs: ['The vault token account for output token'];
                    writable: true;
                    relations: ['pool'];
                },
                {
                    name: 'tokenAMint';
                    docs: ['The mint of token a'];
                },
                {
                    name: 'tokenBMint';
                    docs: ['The mint of token b'];
                },
                {
                    name: 'payer';
                    docs: ['The user performing the swap'];
                    signer: true;
                },
                {
                    name: 'tokenAProgram';
                    docs: ['Token a program'];
                },
                {
                    name: 'tokenBProgram';
                    docs: ['Token b program'];
                },
                {
                    name: 'referralTokenAccount';
                    docs: ['referral token account'];
                    writable: true;
                    optional: true;
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'params';
                    type: {
                        defined: {
                            name: 'swapParameters2';
                        };
                    };
                }
            ];
        },
        {
            name: 'updatePoolFees';
            discriminator: [118, 217, 203, 179, 60, 8, 70, 89];
            accounts: [
                {
                    name: 'pool';
                    writable: true;
                },
                {
                    name: 'operator';
                },
                {
                    name: 'signer';
                    signer: true;
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'params';
                    type: {
                        defined: {
                            name: 'updatePoolFeesParameters';
                        };
                    };
                }
            ];
        },
        {
            name: 'updateRewardDuration';
            discriminator: [138, 174, 196, 169, 213, 235, 254, 107];
            accounts: [
                {
                    name: 'pool';
                    writable: true;
                },
                {
                    name: 'signer';
                    signer: true;
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'rewardIndex';
                    type: 'u8';
                },
                {
                    name: 'newDuration';
                    type: 'u64';
                }
            ];
        },
        {
            name: 'updateRewardFunder';
            discriminator: [211, 28, 48, 32, 215, 160, 35, 23];
            accounts: [
                {
                    name: 'pool';
                    writable: true;
                },
                {
                    name: 'signer';
                    signer: true;
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'rewardIndex';
                    type: 'u8';
                },
                {
                    name: 'newFunder';
                    type: 'pubkey';
                }
            ];
        },
        {
            name: 'withdrawIneligibleReward';
            discriminator: [148, 206, 42, 195, 247, 49, 103, 8];
            accounts: [
                {
                    name: 'poolAuthority';
                    address: 'HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC';
                },
                {
                    name: 'pool';
                    writable: true;
                },
                {
                    name: 'rewardVault';
                    writable: true;
                },
                {
                    name: 'rewardMint';
                },
                {
                    name: 'funderTokenAccount';
                    writable: true;
                },
                {
                    name: 'funder';
                    signer: true;
                },
                {
                    name: 'tokenProgram';
                },
                {
                    name: 'eventAuthority';
                    pda: {
                        seeds: [
                            {
                                kind: 'const';
                                value: [
                                    95,
                                    95,
                                    101,
                                    118,
                                    101,
                                    110,
                                    116,
                                    95,
                                    97,
                                    117,
                                    116,
                                    104,
                                    111,
                                    114,
                                    105,
                                    116,
                                    121
                                ];
                            }
                        ];
                    };
                },
                {
                    name: 'program';
                }
            ];
            args: [
                {
                    name: 'rewardIndex';
                    type: 'u8';
                }
            ];
        },
        {
            name: 'zapProtocolFee';
            discriminator: [213, 155, 187, 34, 56, 182, 91, 240];
            accounts: [
                {
                    name: 'poolAuthority';
                    address: 'HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC';
                },
                {
                    name: 'pool';
                    writable: true;
                },
                {
                    name: 'tokenVault';
                    writable: true;
                },
                {
                    name: 'tokenMint';
                },
                {
                    name: 'receiverToken';
                    writable: true;
                },
                {
                    name: 'operator';
                    docs: ['zap claim fee operator'];
                },
                {
                    name: 'signer';
                    docs: ['operator'];
                    signer: true;
                },
                {
                    name: 'tokenProgram';
                    docs: ['Token program'];
                },
                {
                    name: 'sysvarInstructions';
                    address: 'Sysvar1nstructions1111111111111111111111111';
                }
            ];
            args: [
                {
                    name: 'maxAmount';
                    type: 'u64';
                }
            ];
        }
    ];
    accounts: [
        {
            name: 'config';
            discriminator: [155, 12, 170, 224, 30, 250, 204, 130];
        },
        {
            name: 'operator';
            discriminator: [219, 31, 188, 145, 69, 139, 204, 117];
        },
        {
            name: 'podAlignedFeeMarketCapScheduler';
            discriminator: [251, 130, 208, 253, 245, 27, 145, 203];
        },
        {
            name: 'podAlignedFeeRateLimiter';
            discriminator: [160, 219, 8, 251, 179, 7, 16, 117];
        },
        {
            name: 'podAlignedFeeTimeScheduler';
            discriminator: [239, 132, 138, 213, 67, 154, 130, 70];
        },
        {
            name: 'pool';
            discriminator: [241, 154, 109, 4, 17, 177, 109, 188];
        },
        {
            name: 'position';
            discriminator: [170, 188, 143, 228, 122, 64, 247, 208];
        },
        {
            name: 'tokenBadge';
            discriminator: [116, 219, 204, 229, 249, 116, 255, 150];
        },
        {
            name: 'vesting';
            discriminator: [100, 149, 66, 138, 95, 200, 128, 241];
        }
    ];
    events: [
        {
            name: 'evtClaimPartnerFee';
            discriminator: [118, 99, 77, 10, 226, 1, 1, 87];
        },
        {
            name: 'evtClaimPositionFee';
            discriminator: [198, 182, 183, 52, 97, 12, 49, 56];
        },
        {
            name: 'evtClaimProtocolFee';
            discriminator: [186, 244, 75, 251, 188, 13, 25, 33];
        },
        {
            name: 'evtClaimReward';
            discriminator: [218, 86, 147, 200, 235, 188, 215, 231];
        },
        {
            name: 'evtCloseConfig';
            discriminator: [36, 30, 239, 45, 58, 132, 14, 5];
        },
        {
            name: 'evtClosePosition';
            discriminator: [20, 145, 144, 68, 143, 142, 214, 178];
        },
        {
            name: 'evtCreateConfig';
            discriminator: [131, 207, 180, 174, 180, 73, 165, 54];
        },
        {
            name: 'evtCreateDynamicConfig';
            discriminator: [231, 197, 13, 164, 248, 213, 133, 152];
        },
        {
            name: 'evtCreatePosition';
            discriminator: [156, 15, 119, 198, 29, 181, 221, 55];
        },
        {
            name: 'evtCreateTokenBadge';
            discriminator: [141, 120, 134, 116, 34, 28, 114, 160];
        },
        {
            name: 'evtFundReward';
            discriminator: [104, 233, 237, 122, 199, 191, 121, 85];
        },
        {
            name: 'evtInitializePool';
            discriminator: [228, 50, 246, 85, 203, 66, 134, 37];
        },
        {
            name: 'evtInitializeReward';
            discriminator: [129, 91, 188, 3, 246, 52, 185, 249];
        },
        {
            name: 'evtLiquidityChange';
            discriminator: [197, 171, 78, 127, 224, 211, 87, 13];
        },
        {
            name: 'evtLockPosition';
            discriminator: [168, 63, 108, 83, 219, 82, 2, 200];
        },
        {
            name: 'evtPermanentLockPosition';
            discriminator: [145, 143, 162, 218, 218, 80, 67, 11];
        },
        {
            name: 'evtSetPoolStatus';
            discriminator: [100, 213, 74, 3, 95, 91, 228, 146];
        },
        {
            name: 'evtSplitPosition2';
            discriminator: [165, 32, 203, 174, 72, 100, 233, 103];
        },
        {
            name: 'evtSwap2';
            discriminator: [189, 66, 51, 168, 38, 80, 117, 153];
        },
        {
            name: 'evtUpdatePoolFees';
            discriminator: [76, 165, 246, 102, 102, 217, 156, 44];
        },
        {
            name: 'evtUpdateRewardDuration';
            discriminator: [149, 135, 65, 231, 129, 153, 65, 57];
        },
        {
            name: 'evtUpdateRewardFunder';
            discriminator: [76, 154, 208, 13, 40, 115, 246, 146];
        },
        {
            name: 'evtWithdrawIneligibleReward';
            discriminator: [248, 215, 184, 78, 31, 180, 179, 168];
        }
    ];
    errors: [
        {
            code: 6000;
            name: 'mathOverflow';
            msg: 'Math operation overflow';
        },
        {
            code: 6001;
            name: 'invalidFee';
            msg: 'Invalid fee setup';
        },
        {
            code: 6002;
            name: 'exceededSlippage';
            msg: 'Exceeded slippage tolerance';
        },
        {
            code: 6003;
            name: 'poolDisabled';
            msg: 'Pool disabled';
        },
        {
            code: 6004;
            name: 'exceedMaxFeeBps';
            msg: 'Exceeded max fee bps';
        },
        {
            code: 6005;
            name: 'invalidAdmin';
            msg: 'Invalid admin';
        },
        {
            code: 6006;
            name: 'amountIsZero';
            msg: 'Amount is zero';
        },
        {
            code: 6007;
            name: 'typeCastFailed';
            msg: 'Type cast error';
        },
        {
            code: 6008;
            name: 'unableToModifyActivationPoint';
            msg: 'Unable to modify activation point';
        },
        {
            code: 6009;
            name: 'invalidAuthorityToCreateThePool';
            msg: 'Invalid authority to create the pool';
        },
        {
            code: 6010;
            name: 'invalidActivationType';
            msg: 'Invalid activation type';
        },
        {
            code: 6011;
            name: 'invalidActivationPoint';
            msg: 'Invalid activation point';
        },
        {
            code: 6012;
            name: 'invalidQuoteMint';
            msg: 'Quote token must be SOL,USDC';
        },
        {
            code: 6013;
            name: 'invalidFeeCurve';
            msg: 'Invalid fee curve';
        },
        {
            code: 6014;
            name: 'invalidPriceRange';
            msg: 'Invalid Price Range';
        },
        {
            code: 6015;
            name: 'priceRangeViolation';
            msg: 'Trade is over price range';
        },
        {
            code: 6016;
            name: 'invalidParameters';
            msg: 'Invalid parameters';
        },
        {
            code: 6017;
            name: 'invalidCollectFeeMode';
            msg: 'Invalid collect fee mode';
        },
        {
            code: 6018;
            name: 'invalidInput';
            msg: 'Invalid input';
        },
        {
            code: 6019;
            name: 'cannotCreateTokenBadgeOnSupportedMint';
            msg: 'Cannot create token badge on supported mint';
        },
        {
            code: 6020;
            name: 'invalidTokenBadge';
            msg: 'Invalid token badge';
        },
        {
            code: 6021;
            name: 'invalidMinimumLiquidity';
            msg: 'Invalid minimum liquidity';
        },
        {
            code: 6022;
            name: 'invalidVestingInfo';
            msg: 'Invalid vesting information';
        },
        {
            code: 6023;
            name: 'insufficientLiquidity';
            msg: 'Insufficient liquidity';
        },
        {
            code: 6024;
            name: 'invalidVestingAccount';
            msg: 'Invalid vesting account';
        },
        {
            code: 6025;
            name: 'invalidPoolStatus';
            msg: 'Invalid pool status';
        },
        {
            code: 6026;
            name: 'unsupportNativeMintToken2022';
            msg: 'Unsupported native mint token2022';
        },
        {
            code: 6027;
            name: 'invalidRewardIndex';
            msg: 'Invalid reward index';
        },
        {
            code: 6028;
            name: 'invalidRewardDuration';
            msg: 'Invalid reward duration';
        },
        {
            code: 6029;
            name: 'rewardInitialized';
            msg: 'Reward already initialized';
        },
        {
            code: 6030;
            name: 'rewardUninitialized';
            msg: 'Reward not initialized';
        },
        {
            code: 6031;
            name: 'invalidRewardVault';
            msg: 'Invalid reward vault';
        },
        {
            code: 6032;
            name: 'mustWithdrawnIneligibleReward';
            msg: 'Must withdraw ineligible reward';
        },
        {
            code: 6033;
            name: 'identicalRewardDuration';
            msg: 'Reward duration is the same';
        },
        {
            code: 6034;
            name: 'rewardCampaignInProgress';
            msg: 'Reward campaign in progress';
        },
        {
            code: 6035;
            name: 'identicalFunder';
            msg: 'Identical funder';
        },
        {
            code: 6036;
            name: 'invalidFunder';
            msg: 'Invalid funder';
        },
        {
            code: 6037;
            name: 'rewardNotEnded';
            msg: 'Reward not ended';
        },
        {
            code: 6038;
            name: 'feeInverseIsIncorrect';
            msg: 'Fee inverse is incorrect';
        },
        {
            code: 6039;
            name: 'positionIsNotEmpty';
            msg: 'Position is not empty';
        },
        {
            code: 6040;
            name: 'invalidPoolCreatorAuthority';
            msg: 'Invalid pool creator authority';
        },
        {
            code: 6041;
            name: 'invalidConfigType';
            msg: 'Invalid config type';
        },
        {
            code: 6042;
            name: 'invalidPoolCreator';
            msg: 'Invalid pool creator';
        },
        {
            code: 6043;
            name: 'rewardVaultFrozenSkipRequired';
            msg: 'Reward vault is frozen, must skip reward to proceed';
        },
        {
            code: 6044;
            name: 'invalidSplitPositionParameters';
            msg: 'Invalid parameters for split position';
        },
        {
            code: 6045;
            name: 'unsupportPositionHasVestingLock';
            msg: 'Unsupported split position has vesting lock';
        },
        {
            code: 6046;
            name: 'samePosition';
            msg: 'Same position';
        },
        {
            code: 6047;
            name: 'invalidBaseFeeMode';
            msg: 'Invalid base fee mode';
        },
        {
            code: 6048;
            name: 'invalidFeeRateLimiter';
            msg: 'Invalid fee rate limiter';
        },
        {
            code: 6049;
            name: 'failToValidateSingleSwapInstruction';
            msg: 'Fail to validate single swap instruction in rate limiter';
        },
        {
            code: 6050;
            name: 'invalidFeeTimeScheduler';
            msg: 'Invalid fee scheduler';
        },
        {
            code: 6051;
            name: 'undeterminedError';
            msg: 'Undetermined error';
        },
        {
            code: 6052;
            name: 'invalidPoolVersion';
            msg: 'Invalid pool version';
        },
        {
            code: 6053;
            name: 'invalidAuthority';
            msg: 'Invalid authority to do that action';
        },
        {
            code: 6054;
            name: 'invalidPermission';
            msg: 'Invalid permission';
        },
        {
            code: 6055;
            name: 'invalidFeeMarketCapScheduler';
            msg: 'Invalid fee market cap scheduler';
        },
        {
            code: 6056;
            name: 'cannotUpdateBaseFee';
            msg: 'Cannot update base fee';
        },
        {
            code: 6057;
            name: 'invalidDynamicFeeParameters';
            msg: 'Invalid dynamic fee parameters';
        },
        {
            code: 6058;
            name: 'invalidUpdatePoolFeesParameters';
            msg: 'Invalid update pool fees parameters';
        },
        {
            code: 6059;
            name: 'missingOperatorAccount';
            msg: 'Missing operator account';
        },
        {
            code: 6060;
            name: 'incorrectAta';
            msg: 'Incorrect ATA';
        },
        {
            code: 6061;
            name: 'invalidZapOutParameters';
            msg: 'Invalid zap out parameters';
        },
        {
            code: 6062;
            name: 'invalidWithdrawProtocolFeeZapAccounts';
            msg: 'Invalid withdraw protocol fee zap accounts';
        },
        {
            code: 6063;
            name: 'mintRestrictedFromZap';
            msg: 'SOL,USDC protocol fee cannot be withdrawn via zap';
        },
        {
            code: 6064;
            name: 'cpiDisabled';
            msg: 'CPI disabled';
        },
        {
            code: 6065;
            name: 'missingZapOutInstruction';
            msg: 'Missing zap out instruction';
        },
        {
            code: 6066;
            name: 'invalidZapAccounts';
            msg: 'Invalid zap accounts';
        }
    ];
    types: [
        {
            name: 'addLiquidityParameters';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'liquidityDelta';
                        docs: ['delta liquidity'];
                        type: 'u128';
                    },
                    {
                        name: 'tokenAAmountThreshold';
                        docs: ['maximum token a amount'];
                        type: 'u64';
                    },
                    {
                        name: 'tokenBAmountThreshold';
                        docs: ['maximum token b amount'];
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'baseFeeInfo';
            serialization: 'bytemuck';
            repr: {
                kind: 'c';
            };
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'data';
                        type: {
                            array: ['u8', 32];
                        };
                    }
                ];
            };
        },
        {
            name: 'baseFeeParameters';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'data';
                        type: {
                            array: ['u8', 30];
                        };
                    }
                ];
            };
        },
        {
            name: 'baseFeeStruct';
            serialization: 'bytemuck';
            repr: {
                kind: 'c';
            };
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'baseFeeInfo';
                        type: {
                            defined: {
                                name: 'baseFeeInfo';
                            };
                        };
                    },
                    {
                        name: 'padding1';
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'borshFeeMarketCapScheduler';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'cliffFeeNumerator';
                        type: 'u64';
                    },
                    {
                        name: 'numberOfPeriod';
                        type: 'u16';
                    },
                    {
                        name: 'sqrtPriceStepBps';
                        type: 'u32';
                    },
                    {
                        name: 'schedulerExpirationDuration';
                        type: 'u32';
                    },
                    {
                        name: 'reductionFactor';
                        type: 'u64';
                    },
                    {
                        name: 'baseFeeMode';
                        type: 'u8';
                    },
                    {
                        name: 'padding';
                        type: {
                            array: ['u8', 3];
                        };
                    }
                ];
            };
        },
        {
            name: 'borshFeeRateLimiter';
            docs: [
                'we denote reference_amount = x0, cliff_fee_numerator = c, fee_increment = i',
                'if input_amount <= x0, then fee = input_amount * c',
                '',
                'if input_amount > x0, then input_amount = x0 + (a * x0 + b)',
                'if a < max_index',
                'then fee = x0 * c + x0 * (c + i) + .... + x0 * (c + i*a) + b * (c + i * (a+1))',
                'then fee = x0 * (c + c*a + i*a*(a+1)/2) + b * (c + i * (a+1))',
                '',
                'if a >= max_index',
                'if a = max_index + d, input_amount = x0 + max_index * x0 + (d * x0 + b)',
                'then fee = x0 * (c + c*max_index + i*max_index*(max_index+1)/2) + (d * x0 + b) * MAX_FEE'
            ];
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'cliffFeeNumerator';
                        type: 'u64';
                    },
                    {
                        name: 'feeIncrementBps';
                        type: 'u16';
                    },
                    {
                        name: 'maxLimiterDuration';
                        type: 'u32';
                    },
                    {
                        name: 'maxFeeBps';
                        type: 'u32';
                    },
                    {
                        name: 'referenceAmount';
                        type: 'u64';
                    },
                    {
                        name: 'baseFeeMode';
                        type: 'u8';
                    },
                    {
                        name: 'padding';
                        type: {
                            array: ['u8', 3];
                        };
                    }
                ];
            };
        },
        {
            name: 'borshFeeTimeScheduler';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'cliffFeeNumerator';
                        type: 'u64';
                    },
                    {
                        name: 'numberOfPeriod';
                        type: 'u16';
                    },
                    {
                        name: 'periodFrequency';
                        type: 'u64';
                    },
                    {
                        name: 'reductionFactor';
                        type: 'u64';
                    },
                    {
                        name: 'baseFeeMode';
                        type: 'u8';
                    },
                    {
                        name: 'padding';
                        type: {
                            array: ['u8', 3];
                        };
                    }
                ];
            };
        },
        {
            name: 'config';
            serialization: 'bytemuck';
            repr: {
                kind: 'c';
            };
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'vaultConfigKey';
                        docs: ['Vault config key'];
                        type: 'pubkey';
                    },
                    {
                        name: 'poolCreatorAuthority';
                        docs: [
                            "Only pool_creator_authority can use the current config to initialize new pool. When it's Pubkey::default, it's a public config."
                        ];
                        type: 'pubkey';
                    },
                    {
                        name: 'poolFees';
                        docs: ['Pool fee'];
                        type: {
                            defined: {
                                name: 'poolFeesConfig';
                            };
                        };
                    },
                    {
                        name: 'activationType';
                        docs: ['Activation type'];
                        type: 'u8';
                    },
                    {
                        name: 'collectFeeMode';
                        docs: ['Collect fee mode'];
                        type: 'u8';
                    },
                    {
                        name: 'configType';
                        docs: ['Config type mode, 0 for static, 1 for dynamic'];
                        type: 'u8';
                    },
                    {
                        name: 'padding0';
                        docs: ['padding 0'];
                        type: {
                            array: ['u8', 5];
                        };
                    },
                    {
                        name: 'index';
                        docs: ['config index'];
                        type: 'u64';
                    },
                    {
                        name: 'sqrtMinPrice';
                        docs: ['sqrt min price'];
                        type: 'u128';
                    },
                    {
                        name: 'sqrtMaxPrice';
                        docs: ['sqrt max price'];
                        type: 'u128';
                    },
                    {
                        name: 'padding1';
                        docs: ['Fee curve point', 'Padding for further use'];
                        type: {
                            array: ['u64', 10];
                        };
                    }
                ];
            };
        },
        {
            name: 'dummyParams';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'borshFeeTimeSchedulerParams';
                        type: {
                            defined: {
                                name: 'borshFeeTimeScheduler';
                            };
                        };
                    },
                    {
                        name: 'borshFeeRateLimiterParams';
                        type: {
                            defined: {
                                name: 'borshFeeRateLimiter';
                            };
                        };
                    },
                    {
                        name: 'borshFeeMarketCapSchedulerParams';
                        type: {
                            defined: {
                                name: 'borshFeeMarketCapScheduler';
                            };
                        };
                    }
                ];
            };
        },
        {
            name: 'dynamicConfigParameters';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'poolCreatorAuthority';
                        type: 'pubkey';
                    }
                ];
            };
        },
        {
            name: 'dynamicFeeConfig';
            serialization: 'bytemuck';
            repr: {
                kind: 'c';
            };
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'initialized';
                        type: 'u8';
                    },
                    {
                        name: 'padding';
                        type: {
                            array: ['u8', 7];
                        };
                    },
                    {
                        name: 'maxVolatilityAccumulator';
                        type: 'u32';
                    },
                    {
                        name: 'variableFeeControl';
                        type: 'u32';
                    },
                    {
                        name: 'binStep';
                        type: 'u16';
                    },
                    {
                        name: 'filterPeriod';
                        type: 'u16';
                    },
                    {
                        name: 'decayPeriod';
                        type: 'u16';
                    },
                    {
                        name: 'reductionFactor';
                        type: 'u16';
                    },
                    {
                        name: 'padding1';
                        type: {
                            array: ['u8', 8];
                        };
                    },
                    {
                        name: 'binStepU128';
                        type: 'u128';
                    }
                ];
            };
        },
        {
            name: 'dynamicFeeParameters';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'binStep';
                        type: 'u16';
                    },
                    {
                        name: 'binStepU128';
                        type: 'u128';
                    },
                    {
                        name: 'filterPeriod';
                        type: 'u16';
                    },
                    {
                        name: 'decayPeriod';
                        type: 'u16';
                    },
                    {
                        name: 'reductionFactor';
                        type: 'u16';
                    },
                    {
                        name: 'maxVolatilityAccumulator';
                        type: 'u32';
                    },
                    {
                        name: 'variableFeeControl';
                        type: 'u32';
                    }
                ];
            };
        },
        {
            name: 'dynamicFeeStruct';
            serialization: 'bytemuck';
            repr: {
                kind: 'c';
            };
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'initialized';
                        type: 'u8';
                    },
                    {
                        name: 'padding';
                        type: {
                            array: ['u8', 7];
                        };
                    },
                    {
                        name: 'maxVolatilityAccumulator';
                        type: 'u32';
                    },
                    {
                        name: 'variableFeeControl';
                        type: 'u32';
                    },
                    {
                        name: 'binStep';
                        type: 'u16';
                    },
                    {
                        name: 'filterPeriod';
                        type: 'u16';
                    },
                    {
                        name: 'decayPeriod';
                        type: 'u16';
                    },
                    {
                        name: 'reductionFactor';
                        type: 'u16';
                    },
                    {
                        name: 'lastUpdateTimestamp';
                        type: 'u64';
                    },
                    {
                        name: 'binStepU128';
                        type: 'u128';
                    },
                    {
                        name: 'sqrtPriceReference';
                        type: 'u128';
                    },
                    {
                        name: 'volatilityAccumulator';
                        type: 'u128';
                    },
                    {
                        name: 'volatilityReference';
                        type: 'u128';
                    }
                ];
            };
        },
        {
            name: 'evtClaimPartnerFee';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'pool';
                        type: 'pubkey';
                    },
                    {
                        name: 'tokenAAmount';
                        type: 'u64';
                    },
                    {
                        name: 'tokenBAmount';
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'evtClaimPositionFee';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'pool';
                        type: 'pubkey';
                    },
                    {
                        name: 'position';
                        type: 'pubkey';
                    },
                    {
                        name: 'owner';
                        type: 'pubkey';
                    },
                    {
                        name: 'feeAClaimed';
                        type: 'u64';
                    },
                    {
                        name: 'feeBClaimed';
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'evtClaimProtocolFee';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'pool';
                        type: 'pubkey';
                    },
                    {
                        name: 'tokenAAmount';
                        type: 'u64';
                    },
                    {
                        name: 'tokenBAmount';
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'evtClaimReward';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'pool';
                        type: 'pubkey';
                    },
                    {
                        name: 'position';
                        type: 'pubkey';
                    },
                    {
                        name: 'owner';
                        type: 'pubkey';
                    },
                    {
                        name: 'mintReward';
                        type: 'pubkey';
                    },
                    {
                        name: 'rewardIndex';
                        type: 'u8';
                    },
                    {
                        name: 'totalReward';
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'evtCloseConfig';
            docs: ['Close config'];
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'config';
                        docs: ['Config pubkey'];
                        type: 'pubkey';
                    },
                    {
                        name: 'admin';
                        docs: ['admin pk'];
                        type: 'pubkey';
                    }
                ];
            };
        },
        {
            name: 'evtClosePosition';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'pool';
                        type: 'pubkey';
                    },
                    {
                        name: 'owner';
                        type: 'pubkey';
                    },
                    {
                        name: 'position';
                        type: 'pubkey';
                    },
                    {
                        name: 'positionNftMint';
                        type: 'pubkey';
                    }
                ];
            };
        },
        {
            name: 'evtCreateConfig';
            docs: ['Create static config'];
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'poolFees';
                        type: {
                            defined: {
                                name: 'poolFeeParameters';
                            };
                        };
                    },
                    {
                        name: 'vaultConfigKey';
                        type: 'pubkey';
                    },
                    {
                        name: 'poolCreatorAuthority';
                        type: 'pubkey';
                    },
                    {
                        name: 'activationType';
                        type: 'u8';
                    },
                    {
                        name: 'sqrtMinPrice';
                        type: 'u128';
                    },
                    {
                        name: 'sqrtMaxPrice';
                        type: 'u128';
                    },
                    {
                        name: 'collectFeeMode';
                        type: 'u8';
                    },
                    {
                        name: 'index';
                        type: 'u64';
                    },
                    {
                        name: 'config';
                        type: 'pubkey';
                    }
                ];
            };
        },
        {
            name: 'evtCreateDynamicConfig';
            docs: ['Create dynamic config'];
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'config';
                        type: 'pubkey';
                    },
                    {
                        name: 'poolCreatorAuthority';
                        type: 'pubkey';
                    },
                    {
                        name: 'index';
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'evtCreatePosition';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'pool';
                        type: 'pubkey';
                    },
                    {
                        name: 'owner';
                        type: 'pubkey';
                    },
                    {
                        name: 'position';
                        type: 'pubkey';
                    },
                    {
                        name: 'positionNftMint';
                        type: 'pubkey';
                    }
                ];
            };
        },
        {
            name: 'evtCreateTokenBadge';
            docs: ['Create token badge'];
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'tokenMint';
                        type: 'pubkey';
                    }
                ];
            };
        },
        {
            name: 'evtFundReward';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'pool';
                        type: 'pubkey';
                    },
                    {
                        name: 'funder';
                        type: 'pubkey';
                    },
                    {
                        name: 'mintReward';
                        type: 'pubkey';
                    },
                    {
                        name: 'rewardIndex';
                        type: 'u8';
                    },
                    {
                        name: 'amount';
                        type: 'u64';
                    },
                    {
                        name: 'transferFeeExcludedAmountIn';
                        type: 'u64';
                    },
                    {
                        name: 'rewardDurationEnd';
                        type: 'u64';
                    },
                    {
                        name: 'preRewardRate';
                        type: 'u128';
                    },
                    {
                        name: 'postRewardRate';
                        type: 'u128';
                    }
                ];
            };
        },
        {
            name: 'evtInitializePool';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'pool';
                        type: 'pubkey';
                    },
                    {
                        name: 'tokenAMint';
                        type: 'pubkey';
                    },
                    {
                        name: 'tokenBMint';
                        type: 'pubkey';
                    },
                    {
                        name: 'creator';
                        type: 'pubkey';
                    },
                    {
                        name: 'payer';
                        type: 'pubkey';
                    },
                    {
                        name: 'alphaVault';
                        type: 'pubkey';
                    },
                    {
                        name: 'poolFees';
                        type: {
                            defined: {
                                name: 'poolFeeParameters';
                            };
                        };
                    },
                    {
                        name: 'sqrtMinPrice';
                        type: 'u128';
                    },
                    {
                        name: 'sqrtMaxPrice';
                        type: 'u128';
                    },
                    {
                        name: 'activationType';
                        type: 'u8';
                    },
                    {
                        name: 'collectFeeMode';
                        type: 'u8';
                    },
                    {
                        name: 'liquidity';
                        type: 'u128';
                    },
                    {
                        name: 'sqrtPrice';
                        type: 'u128';
                    },
                    {
                        name: 'activationPoint';
                        type: 'u64';
                    },
                    {
                        name: 'tokenAFlag';
                        type: 'u8';
                    },
                    {
                        name: 'tokenBFlag';
                        type: 'u8';
                    },
                    {
                        name: 'tokenAAmount';
                        type: 'u64';
                    },
                    {
                        name: 'tokenBAmount';
                        type: 'u64';
                    },
                    {
                        name: 'totalAmountA';
                        type: 'u64';
                    },
                    {
                        name: 'totalAmountB';
                        type: 'u64';
                    },
                    {
                        name: 'poolType';
                        type: 'u8';
                    }
                ];
            };
        },
        {
            name: 'evtInitializeReward';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'pool';
                        type: 'pubkey';
                    },
                    {
                        name: 'rewardMint';
                        type: 'pubkey';
                    },
                    {
                        name: 'funder';
                        type: 'pubkey';
                    },
                    {
                        name: 'creator';
                        type: 'pubkey';
                    },
                    {
                        name: 'rewardIndex';
                        type: 'u8';
                    },
                    {
                        name: 'rewardDuration';
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'evtLiquidityChange';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'pool';
                        type: 'pubkey';
                    },
                    {
                        name: 'position';
                        type: 'pubkey';
                    },
                    {
                        name: 'owner';
                        type: 'pubkey';
                    },
                    {
                        name: 'tokenAAmount';
                        type: 'u64';
                    },
                    {
                        name: 'tokenBAmount';
                        type: 'u64';
                    },
                    {
                        name: 'transferFeeIncludedTokenAAmount';
                        type: 'u64';
                    },
                    {
                        name: 'transferFeeIncludedTokenBAmount';
                        type: 'u64';
                    },
                    {
                        name: 'reserveAAmount';
                        type: 'u64';
                    },
                    {
                        name: 'reserveBAmount';
                        type: 'u64';
                    },
                    {
                        name: 'liquidityDelta';
                        type: 'u128';
                    },
                    {
                        name: 'tokenAAmountThreshold';
                        type: 'u64';
                    },
                    {
                        name: 'tokenBAmountThreshold';
                        type: 'u64';
                    },
                    {
                        name: 'changeType';
                        type: 'u8';
                    }
                ];
            };
        },
        {
            name: 'evtLockPosition';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'pool';
                        type: 'pubkey';
                    },
                    {
                        name: 'position';
                        type: 'pubkey';
                    },
                    {
                        name: 'owner';
                        type: 'pubkey';
                    },
                    {
                        name: 'vesting';
                        type: 'pubkey';
                    },
                    {
                        name: 'cliffPoint';
                        type: 'u64';
                    },
                    {
                        name: 'periodFrequency';
                        type: 'u64';
                    },
                    {
                        name: 'cliffUnlockLiquidity';
                        type: 'u128';
                    },
                    {
                        name: 'liquidityPerPeriod';
                        type: 'u128';
                    },
                    {
                        name: 'numberOfPeriod';
                        type: 'u16';
                    }
                ];
            };
        },
        {
            name: 'evtPermanentLockPosition';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'pool';
                        type: 'pubkey';
                    },
                    {
                        name: 'position';
                        type: 'pubkey';
                    },
                    {
                        name: 'lockLiquidityAmount';
                        type: 'u128';
                    },
                    {
                        name: 'totalPermanentLockedLiquidity';
                        type: 'u128';
                    }
                ];
            };
        },
        {
            name: 'evtSetPoolStatus';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'pool';
                        type: 'pubkey';
                    },
                    {
                        name: 'status';
                        type: 'u8';
                    }
                ];
            };
        },
        {
            name: 'evtSplitPosition2';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'pool';
                        type: 'pubkey';
                    },
                    {
                        name: 'firstOwner';
                        type: 'pubkey';
                    },
                    {
                        name: 'secondOwner';
                        type: 'pubkey';
                    },
                    {
                        name: 'firstPosition';
                        type: 'pubkey';
                    },
                    {
                        name: 'secondPosition';
                        type: 'pubkey';
                    },
                    {
                        name: 'currentSqrtPrice';
                        type: 'u128';
                    },
                    {
                        name: 'amountSplits';
                        type: {
                            defined: {
                                name: 'splitAmountInfo';
                            };
                        };
                    },
                    {
                        name: 'firstPositionInfo';
                        type: {
                            defined: {
                                name: 'splitPositionInfo';
                            };
                        };
                    },
                    {
                        name: 'secondPositionInfo';
                        type: {
                            defined: {
                                name: 'splitPositionInfo';
                            };
                        };
                    },
                    {
                        name: 'splitPositionParameters';
                        type: {
                            defined: {
                                name: 'splitPositionParameters2';
                            };
                        };
                    }
                ];
            };
        },
        {
            name: 'evtSwap2';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'pool';
                        type: 'pubkey';
                    },
                    {
                        name: 'tradeDirection';
                        type: 'u8';
                    },
                    {
                        name: 'collectFeeMode';
                        type: 'u8';
                    },
                    {
                        name: 'hasReferral';
                        type: 'bool';
                    },
                    {
                        name: 'params';
                        type: {
                            defined: {
                                name: 'swapParameters2';
                            };
                        };
                    },
                    {
                        name: 'swapResult';
                        type: {
                            defined: {
                                name: 'swapResult2';
                            };
                        };
                    },
                    {
                        name: 'includedTransferFeeAmountIn';
                        type: 'u64';
                    },
                    {
                        name: 'includedTransferFeeAmountOut';
                        type: 'u64';
                    },
                    {
                        name: 'excludedTransferFeeAmountOut';
                        type: 'u64';
                    },
                    {
                        name: 'currentTimestamp';
                        type: 'u64';
                    },
                    {
                        name: 'reserveAAmount';
                        type: 'u64';
                    },
                    {
                        name: 'reserveBAmount';
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'evtUpdatePoolFees';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'pool';
                        type: 'pubkey';
                    },
                    {
                        name: 'operator';
                        type: 'pubkey';
                    },
                    {
                        name: 'params';
                        type: {
                            defined: {
                                name: 'updatePoolFeesParameters';
                            };
                        };
                    }
                ];
            };
        },
        {
            name: 'evtUpdateRewardDuration';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'pool';
                        type: 'pubkey';
                    },
                    {
                        name: 'rewardIndex';
                        type: 'u8';
                    },
                    {
                        name: 'oldRewardDuration';
                        type: 'u64';
                    },
                    {
                        name: 'newRewardDuration';
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'evtUpdateRewardFunder';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'pool';
                        type: 'pubkey';
                    },
                    {
                        name: 'rewardIndex';
                        type: 'u8';
                    },
                    {
                        name: 'oldFunder';
                        type: 'pubkey';
                    },
                    {
                        name: 'newFunder';
                        type: 'pubkey';
                    }
                ];
            };
        },
        {
            name: 'evtWithdrawIneligibleReward';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'pool';
                        type: 'pubkey';
                    },
                    {
                        name: 'rewardMint';
                        type: 'pubkey';
                    },
                    {
                        name: 'amount';
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'initializeCustomizablePoolParameters';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'poolFees';
                        docs: ['pool fees'];
                        type: {
                            defined: {
                                name: 'poolFeeParameters';
                            };
                        };
                    },
                    {
                        name: 'sqrtMinPrice';
                        docs: ['sqrt min price'];
                        type: 'u128';
                    },
                    {
                        name: 'sqrtMaxPrice';
                        docs: ['sqrt max price'];
                        type: 'u128';
                    },
                    {
                        name: 'hasAlphaVault';
                        docs: ['has alpha vault'];
                        type: 'bool';
                    },
                    {
                        name: 'liquidity';
                        docs: ['initialize liquidity'];
                        type: 'u128';
                    },
                    {
                        name: 'sqrtPrice';
                        docs: [
                            'The init price of the pool as a sqrt(token_b/token_a) Q64.64 value. Market cap fee scheduler minimum price will be derived from this value'
                        ];
                        type: 'u128';
                    },
                    {
                        name: 'activationType';
                        docs: ['activation type'];
                        type: 'u8';
                    },
                    {
                        name: 'collectFeeMode';
                        docs: ['collect fee mode'];
                        type: 'u8';
                    },
                    {
                        name: 'activationPoint';
                        docs: ['activation point'];
                        type: {
                            option: 'u64';
                        };
                    }
                ];
            };
        },
        {
            name: 'initializePoolParameters';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'liquidity';
                        docs: ['initialize liquidity'];
                        type: 'u128';
                    },
                    {
                        name: 'sqrtPrice';
                        docs: [
                            'The init price of the pool as a sqrt(token_b/token_a) Q64.64 value'
                        ];
                        type: 'u128';
                    },
                    {
                        name: 'activationPoint';
                        docs: ['activation point'];
                        type: {
                            option: 'u64';
                        };
                    }
                ];
            };
        },
        {
            name: 'operator';
            serialization: 'bytemuck';
            repr: {
                kind: 'c';
            };
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'whitelistedAddress';
                        type: 'pubkey';
                    },
                    {
                        name: 'permission';
                        type: 'u128';
                    },
                    {
                        name: 'padding';
                        type: {
                            array: ['u64', 2];
                        };
                    }
                ];
            };
        },
        {
            name: 'podAlignedFeeMarketCapScheduler';
            serialization: 'bytemuck';
            repr: {
                kind: 'c';
            };
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'cliffFeeNumerator';
                        type: 'u64';
                    },
                    {
                        name: 'baseFeeMode';
                        type: 'u8';
                    },
                    {
                        name: 'padding';
                        type: {
                            array: ['u8', 5];
                        };
                    },
                    {
                        name: 'numberOfPeriod';
                        type: 'u16';
                    },
                    {
                        name: 'sqrtPriceStepBps';
                        type: 'u32';
                    },
                    {
                        name: 'schedulerExpirationDuration';
                        type: 'u32';
                    },
                    {
                        name: 'reductionFactor';
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'podAlignedFeeRateLimiter';
            serialization: 'bytemuck';
            repr: {
                kind: 'c';
            };
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'cliffFeeNumerator';
                        type: 'u64';
                    },
                    {
                        name: 'baseFeeMode';
                        type: 'u8';
                    },
                    {
                        name: 'padding';
                        type: {
                            array: ['u8', 5];
                        };
                    },
                    {
                        name: 'feeIncrementBps';
                        type: 'u16';
                    },
                    {
                        name: 'maxLimiterDuration';
                        type: 'u32';
                    },
                    {
                        name: 'maxFeeBps';
                        type: 'u32';
                    },
                    {
                        name: 'referenceAmount';
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'podAlignedFeeTimeScheduler';
            serialization: 'bytemuck';
            repr: {
                kind: 'c';
            };
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'cliffFeeNumerator';
                        type: 'u64';
                    },
                    {
                        name: 'baseFeeMode';
                        type: 'u8';
                    },
                    {
                        name: 'padding';
                        type: {
                            array: ['u8', 5];
                        };
                    },
                    {
                        name: 'numberOfPeriod';
                        type: 'u16';
                    },
                    {
                        name: 'periodFrequency';
                        type: 'u64';
                    },
                    {
                        name: 'reductionFactor';
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'pool';
            serialization: 'bytemuck';
            repr: {
                kind: 'c';
            };
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'poolFees';
                        docs: ['Pool fee'];
                        type: {
                            defined: {
                                name: 'poolFeesStruct';
                            };
                        };
                    },
                    {
                        name: 'tokenAMint';
                        docs: ['token a mint'];
                        type: 'pubkey';
                    },
                    {
                        name: 'tokenBMint';
                        docs: ['token b mint'];
                        type: 'pubkey';
                    },
                    {
                        name: 'tokenAVault';
                        docs: ['token a vault'];
                        type: 'pubkey';
                    },
                    {
                        name: 'tokenBVault';
                        docs: ['token b vault'];
                        type: 'pubkey';
                    },
                    {
                        name: 'whitelistedVault';
                        docs: [
                            'Whitelisted vault to be able to buy pool before activation_point'
                        ];
                        type: 'pubkey';
                    },
                    {
                        name: 'partner';
                        docs: ['partner'];
                        type: 'pubkey';
                    },
                    {
                        name: 'liquidity';
                        docs: ['liquidity share'];
                        type: 'u128';
                    },
                    {
                        name: 'padding';
                        docs: [
                            'padding, previous reserve amount, be careful to use that field'
                        ];
                        type: 'u128';
                    },
                    {
                        name: 'protocolAFee';
                        docs: ['protocol a fee'];
                        type: 'u64';
                    },
                    {
                        name: 'protocolBFee';
                        docs: ['protocol b fee'];
                        type: 'u64';
                    },
                    {
                        name: 'partnerAFee';
                        docs: ['partner a fee'];
                        type: 'u64';
                    },
                    {
                        name: 'partnerBFee';
                        docs: ['partner b fee'];
                        type: 'u64';
                    },
                    {
                        name: 'sqrtMinPrice';
                        docs: ['min price'];
                        type: 'u128';
                    },
                    {
                        name: 'sqrtMaxPrice';
                        docs: ['max price'];
                        type: 'u128';
                    },
                    {
                        name: 'sqrtPrice';
                        docs: ['current price'];
                        type: 'u128';
                    },
                    {
                        name: 'activationPoint';
                        docs: ['Activation point, can be slot or timestamp'];
                        type: 'u64';
                    },
                    {
                        name: 'activationType';
                        docs: [
                            'Activation type, 0 means by slot, 1 means by timestamp'
                        ];
                        type: 'u8';
                    },
                    {
                        name: 'poolStatus';
                        docs: ['pool status, 0: enable, 1 disable'];
                        type: 'u8';
                    },
                    {
                        name: 'tokenAFlag';
                        docs: ['token a flag'];
                        type: 'u8';
                    },
                    {
                        name: 'tokenBFlag';
                        docs: ['token b flag'];
                        type: 'u8';
                    },
                    {
                        name: 'collectFeeMode';
                        docs: [
                            '0 is collect fee in both token, 1 only collect fee only in token b'
                        ];
                        type: 'u8';
                    },
                    {
                        name: 'poolType';
                        docs: ['pool type'];
                        type: 'u8';
                    },
                    {
                        name: 'version';
                        docs: [
                            'pool version, 0: max_fee is still capped at 50%, 1: max_fee is capped at 99%'
                        ];
                        type: 'u8';
                    },
                    {
                        name: 'padding0';
                        docs: ['padding'];
                        type: 'u8';
                    },
                    {
                        name: 'feeAPerLiquidity';
                        docs: ['cumulative'];
                        type: {
                            array: ['u8', 32];
                        };
                    },
                    {
                        name: 'feeBPerLiquidity';
                        docs: ['cumulative'];
                        type: {
                            array: ['u8', 32];
                        };
                    },
                    {
                        name: 'permanentLockLiquidity';
                        type: 'u128';
                    },
                    {
                        name: 'metrics';
                        docs: ['metrics'];
                        type: {
                            defined: {
                                name: 'poolMetrics';
                            };
                        };
                    },
                    {
                        name: 'creator';
                        docs: ['pool creator'];
                        type: 'pubkey';
                    },
                    {
                        name: 'padding1';
                        docs: ['Padding for further use'];
                        type: {
                            array: ['u64', 6];
                        };
                    },
                    {
                        name: 'rewardInfos';
                        docs: ['Farming reward information'];
                        type: {
                            array: [
                                {
                                    defined: {
                                        name: 'rewardInfo';
                                    };
                                },
                                2
                            ];
                        };
                    }
                ];
            };
        },
        {
            name: 'poolFeeParameters';
            docs: ['Information regarding fee charges'];
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'baseFee';
                        docs: ['Base fee'];
                        type: {
                            defined: {
                                name: 'baseFeeParameters';
                            };
                        };
                    },
                    {
                        name: 'dynamicFee';
                        docs: ['dynamic fee'];
                        type: {
                            option: {
                                defined: {
                                    name: 'dynamicFeeParameters';
                                };
                            };
                        };
                    }
                ];
            };
        },
        {
            name: 'poolFeesConfig';
            serialization: 'bytemuck';
            repr: {
                kind: 'c';
            };
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'baseFee';
                        type: {
                            defined: {
                                name: 'baseFeeInfo';
                            };
                        };
                    },
                    {
                        name: 'dynamicFee';
                        type: {
                            defined: {
                                name: 'dynamicFeeConfig';
                            };
                        };
                    },
                    {
                        name: 'protocolFeePercent';
                        type: 'u8';
                    },
                    {
                        name: 'partnerFeePercent';
                        type: 'u8';
                    },
                    {
                        name: 'referralFeePercent';
                        type: 'u8';
                    },
                    {
                        name: 'padding0';
                        type: {
                            array: ['u8', 5];
                        };
                    },
                    {
                        name: 'padding1';
                        type: {
                            array: ['u64', 5];
                        };
                    }
                ];
            };
        },
        {
            name: 'poolFeesStruct';
            docs: [
                'Information regarding fee charges',
                'trading_fee = amount * trade_fee_numerator / denominator',
                'protocol_fee = trading_fee * protocol_fee_percentage / 100',
                'referral_fee = protocol_fee * referral_percentage / 100',
                'partner_fee = (protocol_fee - referral_fee) * partner_fee_percentage / denominator'
            ];
            serialization: 'bytemuck';
            repr: {
                kind: 'c';
            };
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'baseFee';
                        docs: [
                            'Trade fees are extra token amounts that are held inside the token',
                            'accounts during a trade, making the value of liquidity tokens rise.',
                            'Trade fee numerator'
                        ];
                        type: {
                            defined: {
                                name: 'baseFeeStruct';
                            };
                        };
                    },
                    {
                        name: 'protocolFeePercent';
                        docs: [
                            'Protocol trading fees are extra token amounts that are held inside the token',
                            'accounts during a trade, with the equivalent in pool tokens minted to',
                            'the protocol of the program.',
                            'Protocol trade fee numerator'
                        ];
                        type: 'u8';
                    },
                    {
                        name: 'partnerFeePercent';
                        docs: ['partner fee'];
                        type: 'u8';
                    },
                    {
                        name: 'referralFeePercent';
                        docs: ['referral fee'];
                        type: 'u8';
                    },
                    {
                        name: 'padding0';
                        docs: ['padding'];
                        type: {
                            array: ['u8', 5];
                        };
                    },
                    {
                        name: 'dynamicFee';
                        docs: ['dynamic fee'];
                        type: {
                            defined: {
                                name: 'dynamicFeeStruct';
                            };
                        };
                    },
                    {
                        name: 'initSqrtPrice';
                        type: 'u128';
                    }
                ];
            };
        },
        {
            name: 'poolMetrics';
            serialization: 'bytemuck';
            repr: {
                kind: 'c';
            };
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'totalLpAFee';
                        type: 'u128';
                    },
                    {
                        name: 'totalLpBFee';
                        type: 'u128';
                    },
                    {
                        name: 'totalProtocolAFee';
                        type: 'u64';
                    },
                    {
                        name: 'totalProtocolBFee';
                        type: 'u64';
                    },
                    {
                        name: 'totalPartnerAFee';
                        type: 'u64';
                    },
                    {
                        name: 'totalPartnerBFee';
                        type: 'u64';
                    },
                    {
                        name: 'totalPosition';
                        type: 'u64';
                    },
                    {
                        name: 'padding';
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'position';
            serialization: 'bytemuck';
            repr: {
                kind: 'c';
            };
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'pool';
                        type: 'pubkey';
                    },
                    {
                        name: 'nftMint';
                        docs: ['nft mint'];
                        type: 'pubkey';
                    },
                    {
                        name: 'feeAPerTokenCheckpoint';
                        docs: ['fee a checkpoint'];
                        type: {
                            array: ['u8', 32];
                        };
                    },
                    {
                        name: 'feeBPerTokenCheckpoint';
                        docs: ['fee b checkpoint'];
                        type: {
                            array: ['u8', 32];
                        };
                    },
                    {
                        name: 'feeAPending';
                        docs: ['fee a pending'];
                        type: 'u64';
                    },
                    {
                        name: 'feeBPending';
                        docs: ['fee b pending'];
                        type: 'u64';
                    },
                    {
                        name: 'unlockedLiquidity';
                        docs: ['unlock liquidity'];
                        type: 'u128';
                    },
                    {
                        name: 'vestedLiquidity';
                        docs: ['vesting liquidity'];
                        type: 'u128';
                    },
                    {
                        name: 'permanentLockedLiquidity';
                        docs: ['permanent locked liquidity'];
                        type: 'u128';
                    },
                    {
                        name: 'metrics';
                        docs: ['metrics'];
                        type: {
                            defined: {
                                name: 'positionMetrics';
                            };
                        };
                    },
                    {
                        name: 'rewardInfos';
                        docs: ['Farming reward information'];
                        type: {
                            array: [
                                {
                                    defined: {
                                        name: 'userRewardInfo';
                                    };
                                },
                                2
                            ];
                        };
                    },
                    {
                        name: 'padding';
                        docs: ['padding for future usage'];
                        type: {
                            array: ['u128', 6];
                        };
                    }
                ];
            };
        },
        {
            name: 'positionMetrics';
            serialization: 'bytemuck';
            repr: {
                kind: 'c';
            };
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'totalClaimedAFee';
                        type: 'u64';
                    },
                    {
                        name: 'totalClaimedBFee';
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'removeLiquidityParameters';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'liquidityDelta';
                        docs: ['delta liquidity'];
                        type: 'u128';
                    },
                    {
                        name: 'tokenAAmountThreshold';
                        docs: ['minimum token a amount'];
                        type: 'u64';
                    },
                    {
                        name: 'tokenBAmountThreshold';
                        docs: ['minimum token b amount'];
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'rewardInfo';
            docs: [
                'Stores the state relevant for tracking liquidity mining rewards'
            ];
            serialization: 'bytemuck';
            repr: {
                kind: 'c';
            };
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'initialized';
                        docs: ['Indicates if the reward has been initialized'];
                        type: 'u8';
                    },
                    {
                        name: 'rewardTokenFlag';
                        docs: ['reward token flag'];
                        type: 'u8';
                    },
                    {
                        name: 'padding0';
                        docs: ['padding'];
                        type: {
                            array: ['u8', 6];
                        };
                    },
                    {
                        name: 'padding1';
                        docs: [
                            'Padding to ensure `reward_rate: u128` is 16-byte aligned'
                        ];
                        type: {
                            array: ['u8', 8];
                        };
                    },
                    {
                        name: 'mint';
                        docs: ['Reward token mint.'];
                        type: 'pubkey';
                    },
                    {
                        name: 'vault';
                        docs: ['Reward vault token account.'];
                        type: 'pubkey';
                    },
                    {
                        name: 'funder';
                        docs: ['Authority account that allows to fund rewards'];
                        type: 'pubkey';
                    },
                    {
                        name: 'rewardDuration';
                        docs: ['reward duration'];
                        type: 'u64';
                    },
                    {
                        name: 'rewardDurationEnd';
                        docs: ['reward duration end'];
                        type: 'u64';
                    },
                    {
                        name: 'rewardRate';
                        docs: ['reward rate'];
                        type: 'u128';
                    },
                    {
                        name: 'rewardPerTokenStored';
                        docs: ['Reward per token stored'];
                        type: {
                            array: ['u8', 32];
                        };
                    },
                    {
                        name: 'lastUpdateTime';
                        docs: ['The last time reward states were updated.'];
                        type: 'u64';
                    },
                    {
                        name: 'cumulativeSecondsWithEmptyLiquidityReward';
                        docs: [
                            'Accumulated seconds when the farm distributed rewards but the bin was empty.',
                            'These rewards will be carried over to the next reward time window.'
                        ];
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'splitAmountInfo';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'permanentLockedLiquidity';
                        type: 'u128';
                    },
                    {
                        name: 'unlockedLiquidity';
                        type: 'u128';
                    },
                    {
                        name: 'feeA';
                        type: 'u64';
                    },
                    {
                        name: 'feeB';
                        type: 'u64';
                    },
                    {
                        name: 'reward0';
                        type: 'u64';
                    },
                    {
                        name: 'reward1';
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'splitPositionInfo';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'liquidity';
                        type: 'u128';
                    },
                    {
                        name: 'feeA';
                        type: 'u64';
                    },
                    {
                        name: 'feeB';
                        type: 'u64';
                    },
                    {
                        name: 'reward0';
                        type: 'u64';
                    },
                    {
                        name: 'reward1';
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'splitPositionParameters';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'unlockedLiquidityPercentage';
                        docs: [
                            'Percentage of unlocked liquidity to split to the second position'
                        ];
                        type: 'u8';
                    },
                    {
                        name: 'permanentLockedLiquidityPercentage';
                        docs: [
                            'Percentage of permanent locked liquidity to split to the second position'
                        ];
                        type: 'u8';
                    },
                    {
                        name: 'feeAPercentage';
                        docs: [
                            'Percentage of fee A pending to split to the second position'
                        ];
                        type: 'u8';
                    },
                    {
                        name: 'feeBPercentage';
                        docs: [
                            'Percentage of fee B pending to split to the second position'
                        ];
                        type: 'u8';
                    },
                    {
                        name: 'reward0Percentage';
                        docs: [
                            'Percentage of reward 0 pending to split to the second position'
                        ];
                        type: 'u8';
                    },
                    {
                        name: 'reward1Percentage';
                        docs: [
                            'Percentage of reward 1 pending to split to the second position'
                        ];
                        type: 'u8';
                    },
                    {
                        name: 'padding';
                        docs: ['padding for future'];
                        type: {
                            array: ['u8', 16];
                        };
                    }
                ];
            };
        },
        {
            name: 'splitPositionParameters2';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'unlockedLiquidityNumerator';
                        type: 'u32';
                    },
                    {
                        name: 'permanentLockedLiquidityNumerator';
                        type: 'u32';
                    },
                    {
                        name: 'feeANumerator';
                        type: 'u32';
                    },
                    {
                        name: 'feeBNumerator';
                        type: 'u32';
                    },
                    {
                        name: 'reward0Numerator';
                        type: 'u32';
                    },
                    {
                        name: 'reward1Numerator';
                        type: 'u32';
                    }
                ];
            };
        },
        {
            name: 'staticConfigParameters';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'poolFees';
                        type: {
                            defined: {
                                name: 'poolFeeParameters';
                            };
                        };
                    },
                    {
                        name: 'sqrtMinPrice';
                        type: 'u128';
                    },
                    {
                        name: 'sqrtMaxPrice';
                        type: 'u128';
                    },
                    {
                        name: 'vaultConfigKey';
                        type: 'pubkey';
                    },
                    {
                        name: 'poolCreatorAuthority';
                        type: 'pubkey';
                    },
                    {
                        name: 'activationType';
                        type: 'u8';
                    },
                    {
                        name: 'collectFeeMode';
                        type: 'u8';
                    }
                ];
            };
        },
        {
            name: 'swapParameters';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'amountIn';
                        type: 'u64';
                    },
                    {
                        name: 'minimumAmountOut';
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'swapParameters2';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'amount0';
                        docs: [
                            "When it's exact in, partial fill, this will be amount_in. When it's exact out, this will be amount_out"
                        ];
                        type: 'u64';
                    },
                    {
                        name: 'amount1';
                        docs: [
                            "When it's exact in, partial fill, this will be minimum_amount_out. When it's exact out, this will be maximum_amount_in"
                        ];
                        type: 'u64';
                    },
                    {
                        name: 'swapMode';
                        docs: ['Swap mode, refer [SwapMode]'];
                        type: 'u8';
                    }
                ];
            };
        },
        {
            name: 'swapResult2';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'includedFeeInputAmount';
                        type: 'u64';
                    },
                    {
                        name: 'excludedFeeInputAmount';
                        type: 'u64';
                    },
                    {
                        name: 'amountLeft';
                        type: 'u64';
                    },
                    {
                        name: 'outputAmount';
                        type: 'u64';
                    },
                    {
                        name: 'nextSqrtPrice';
                        type: 'u128';
                    },
                    {
                        name: 'tradingFee';
                        type: 'u64';
                    },
                    {
                        name: 'protocolFee';
                        type: 'u64';
                    },
                    {
                        name: 'partnerFee';
                        type: 'u64';
                    },
                    {
                        name: 'referralFee';
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'tokenBadge';
            docs: ['Parameter that set by the protocol'];
            serialization: 'bytemuck';
            repr: {
                kind: 'c';
            };
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'tokenMint';
                        docs: ['token mint'];
                        type: 'pubkey';
                    },
                    {
                        name: 'padding';
                        docs: ['Reserve'];
                        type: {
                            array: ['u8', 128];
                        };
                    }
                ];
            };
        },
        {
            name: 'updatePoolFeesParameters';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'cliffFeeNumerator';
                        docs: [
                            'Base fee update mode:',
                            '- None: skip base fee update',
                            '- Some: update new cliff_fee_numerator if base fee is static'
                        ];
                        type: {
                            option: 'u64';
                        };
                    },
                    {
                        name: 'dynamicFee';
                        docs: [
                            'Dynamic fee update mode:',
                            '- None: skip dynamic fee update',
                            '- Some(with default value): disable dynamic fee',
                            '- Some(with non default value): enable dynamic fee if disabled or update dynamic fee if enabled'
                        ];
                        type: {
                            option: {
                                defined: {
                                    name: 'dynamicFeeParameters';
                                };
                            };
                        };
                    }
                ];
            };
        },
        {
            name: 'userRewardInfo';
            serialization: 'bytemuck';
            repr: {
                kind: 'c';
            };
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'rewardPerTokenCheckpoint';
                        docs: ['The latest update reward checkpoint'];
                        type: {
                            array: ['u8', 32];
                        };
                    },
                    {
                        name: 'rewardPendings';
                        docs: ['Current pending rewards'];
                        type: 'u64';
                    },
                    {
                        name: 'totalClaimedRewards';
                        docs: ['Total claimed rewards'];
                        type: 'u64';
                    }
                ];
            };
        },
        {
            name: 'vesting';
            serialization: 'bytemuck';
            repr: {
                kind: 'c';
            };
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'position';
                        type: 'pubkey';
                    },
                    {
                        name: 'cliffPoint';
                        type: 'u64';
                    },
                    {
                        name: 'periodFrequency';
                        type: 'u64';
                    },
                    {
                        name: 'cliffUnlockLiquidity';
                        type: 'u128';
                    },
                    {
                        name: 'liquidityPerPeriod';
                        type: 'u128';
                    },
                    {
                        name: 'totalReleasedLiquidity';
                        type: 'u128';
                    },
                    {
                        name: 'numberOfPeriod';
                        type: 'u16';
                    },
                    {
                        name: 'padding';
                        type: {
                            array: ['u8', 14];
                        };
                    },
                    {
                        name: 'padding2';
                        type: {
                            array: ['u128', 4];
                        };
                    }
                ];
            };
        },
        {
            name: 'vestingParameters';
            type: {
                kind: 'struct';
                fields: [
                    {
                        name: 'cliffPoint';
                        type: {
                            option: 'u64';
                        };
                    },
                    {
                        name: 'periodFrequency';
                        type: 'u64';
                    },
                    {
                        name: 'cliffUnlockLiquidity';
                        type: 'u128';
                    },
                    {
                        name: 'liquidityPerPeriod';
                        type: 'u128';
                    },
                    {
                        name: 'numberOfPeriod';
                        type: 'u16';
                    }
                ];
            };
        }
    ];
    constants: [
        {
            name: 'binStepBpsDefault';
            type: 'u16';
            value: '1';
        },
        {
            name: 'binStepU128DefaultLeBytes';
            type: {
                array: ['u8', 16];
            };
            value: '[203, 16, 199, 186, 184, 141, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0]';
        },
        {
            name: 'customizablePoolPrefix';
            type: 'bytes';
            value: '[99, 112, 111, 111, 108]';
        },
        {
            name: 'feeDenominator';
            docs: [
                'Default fee denominator. DO NOT simply update it as it will break logic that depends on it as default value.'
            ];
            type: 'u64';
            value: '1000000000';
        },
        {
            name: 'maxBasisPoint';
            docs: ['Max basis point. 100% in pct'];
            type: 'u64';
            value: '10000';
        },
        {
            name: 'maxSqrtPriceLeBytes';
            type: {
                array: ['u8', 16];
            };
            value: '[155, 87, 105, 78, 169, 26, 92, 132, 177, 196, 254, 255, 0, 0, 0, 0]';
        },
        {
            name: 'minSqrtPriceLeBytes';
            type: {
                array: ['u8', 16];
            };
            value: '[80, 59, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]';
        },
        {
            name: 'poolAuthorityPrefix';
            type: 'bytes';
            value: '[112, 111, 111, 108, 95, 97, 117, 116, 104, 111, 114, 105, 116, 121]';
        },
        {
            name: 'poolPrefix';
            type: 'bytes';
            value: '[112, 111, 111, 108]';
        },
        {
            name: 'positionNftAccountPrefix';
            type: 'bytes';
            value: '[112, 111, 115, 105, 116, 105, 111, 110, 95, 110, 102, 116, 95, 97, 99, 99, 111, 117, 110, 116]';
        },
        {
            name: 'positionPrefix';
            type: 'bytes';
            value: '[112, 111, 115, 105, 116, 105, 111, 110]';
        },
        {
            name: 'splitPositionDenominator';
            type: 'u32';
            value: '1000000000';
        },
        {
            name: 'tokenVaultPrefix';
            type: 'bytes';
            value: '[116, 111, 107, 101, 110, 95, 118, 97, 117, 108, 116]';
        }
    ];
};

declare function createClawlabProgram(connection: Connection): {
    program: Program<Clawlab>;
};
/**
 * Create a DAMM V2 program instance
 * @param connection - The connection to the network
 * @param commitment - The commitment level
 * @returns The DAMM V2 program instance
 */
declare function createDammV2Program(connection: Connection): Program<CpAmm>;

/**
 * Get or create an ATA instruction
 * @param connection - The connection
 * @param tokenMint - The token mint
 * @param owner - The owner
 * @param payer - The payer
 * @param allowOwnerOffCurve - Whether to allow the owner to be off curve
 * @param tokenProgram - The token program
 * @returns The ATA instruction
 */
declare const getOrCreateATAInstruction: (connection: Connection, tokenMint: PublicKey, owner: PublicKey, payer: PublicKey, allowOwnerOffCurve: boolean | undefined, tokenProgram: PublicKey) => Promise<{
    ataPubkey: PublicKey;
    ix?: TransactionInstruction;
}>;
/**
 * Unwrap SOL instruction
 * @param owner - The owner of the SOL
 * @param receiver - The receiver of the SOL
 * @param allowOwnerOffCurve - Whether to allow the owner to be off curve
 * @returns The unwrap SOL instruction
 */
declare function unwrapSOLInstruction(owner: PublicKey, receiver: PublicKey, allowOwnerOffCurve?: boolean): TransactionInstruction | null;
/**
 * Wrap SOL instruction
 * @param from - The from address
 * @param to - The to address
 * @param amount - The amount to wrap
 * @returns The wrap SOL instruction
 */
declare function wrapSOLInstruction(from: PublicKey, to: PublicKey, amount: bigint): TransactionInstruction[];
/**
 * Find the associated token address for a wallet and token mint
 * @param walletAddress - The wallet address
 * @param tokenMintAddress - The token mint address
 * @param tokenProgramId - The token program ID
 * @returns The associated token address
 */
declare function findAssociatedTokenAddress(walletAddress: PublicKey, tokenMintAddress: PublicKey, tokenProgramId: PublicKey): PublicKey;

declare function deriveConfig(): PublicKey;
declare function derivePoolAuthority(): PublicKey;
declare function deriveEventAuthority(): PublicKey;
declare function derivePool(baseMint: PublicKey, quoteMint: PublicKey): PublicKey;
declare function deriveBaseVault(baseMint: PublicKey, config: PublicKey): PublicKey;
declare function deriveQuoteVault(quoteMint: PublicKey, config: PublicKey): PublicKey;
declare function deriveUserTokenAccount(baseMint: PublicKey, user: PublicKey): PublicKey;
declare function deriveMintMetadata(baseMint: PublicKey): PublicKey;

var address = "J88VV7gYpBiV2nqt3mUeAwc9hCgB6YoVmqaVAamJRTb7";
var metadata = {
	name: "clawlab",
	version: "0.1.0",
	spec: "0.1.0",
	description: "Created with Anchor"
};
var instructions = [
	{
		name: "buy_token",
		discriminator: [
			138,
			127,
			14,
			91,
			38,
			87,
			115,
			105
		],
		accounts: [
			{
				name: "payer",
				writable: true,
				signer: true
			},
			{
				name: "pool_authority",
				address: "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB"
			},
			{
				name: "config",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								99,
								111,
								110,
								102,
								105,
								103
							]
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "base_mint",
				writable: true
			},
			{
				name: "quote_mint"
			},
			{
				name: "pool",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								112,
								111,
								111,
								108
							]
						},
						{
							kind: "account",
							path: "base_mint"
						},
						{
							kind: "account",
							path: "quote_mint"
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "base_vault",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								98,
								97,
								115,
								101,
								95,
								118,
								97,
								117,
								108,
								116
							]
						},
						{
							kind: "account",
							path: "config"
						},
						{
							kind: "account",
							path: "base_mint"
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "quote_vault",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								113,
								117,
								111,
								116,
								101,
								95,
								118,
								97,
								117,
								108,
								116
							]
						},
						{
							kind: "account",
							path: "config"
						},
						{
							kind: "account",
							path: "quote_mint"
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "input_token_account",
				writable: true
			},
			{
				name: "output_token_account",
				writable: true
			},
			{
				name: "user_token_account",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								117,
								115,
								101,
								114,
								95,
								116,
								111,
								107,
								101,
								110,
								95,
								97,
								99,
								99,
								111,
								117,
								110,
								116
							]
						},
						{
							kind: "account",
							path: "base_mint"
						},
						{
							kind: "account",
							path: "payer"
						}
					]
				}
			},
			{
				name: "token_base_program"
			},
			{
				name: "token_quote_program"
			},
			{
				name: "system_program",
				address: "11111111111111111111111111111111"
			},
			{
				name: "event_authority",
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								95,
								95,
								101,
								118,
								101,
								110,
								116,
								95,
								97,
								117,
								116,
								104,
								111,
								114,
								105,
								116,
								121
							]
						}
					]
				}
			},
			{
				name: "program"
			}
		],
		args: [
			{
				name: "parameters",
				type: {
					defined: {
						name: "BuyTokenParameters"
					}
				}
			}
		]
	},
	{
		name: "claim_authority",
		discriminator: [
			222,
			132,
			185,
			123,
			127,
			107,
			6,
			31
		],
		accounts: [
			{
				name: "payer",
				writable: true,
				signer: true
			},
			{
				name: "pool_authority",
				writable: true,
				address: "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB"
			},
			{
				name: "system_program",
				address: "11111111111111111111111111111111"
			},
			{
				name: "event_authority",
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								95,
								95,
								101,
								118,
								101,
								110,
								116,
								95,
								97,
								117,
								116,
								104,
								111,
								114,
								105,
								116,
								121
							]
						}
					]
				}
			},
			{
				name: "program"
			}
		],
		args: [
		]
	},
	{
		name: "claim_cpamm_pool",
		discriminator: [
			68,
			75,
			169,
			205,
			40,
			228,
			159,
			101
		],
		accounts: [
			{
				name: "payer",
				writable: true,
				signer: true
			},
			{
				name: "pool_authority",
				address: "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB"
			},
			{
				name: "config",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								99,
								111,
								110,
								102,
								105,
								103
							]
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "base_mint",
				writable: true
			},
			{
				name: "quote_mint"
			},
			{
				name: "pool",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								112,
								111,
								111,
								108
							]
						},
						{
							kind: "account",
							path: "base_mint"
						},
						{
							kind: "account",
							path: "quote_mint"
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "base_vault",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								98,
								97,
								115,
								101,
								95,
								118,
								97,
								117,
								108,
								116
							]
						},
						{
							kind: "account",
							path: "config"
						},
						{
							kind: "account",
							path: "base_mint"
						}
					]
				}
			},
			{
				name: "quote_vault",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								113,
								117,
								111,
								116,
								101,
								95,
								118,
								97,
								117,
								108,
								116
							]
						},
						{
							kind: "account",
							path: "config"
						},
						{
							kind: "account",
							path: "quote_mint"
						}
					]
				}
			},
			{
				name: "token_base_program"
			},
			{
				name: "token_quote_program"
			},
			{
				name: "cp_amm_pool_authority",
				docs: [
					"meteora"
				]
			},
			{
				name: "cp_amm_pool"
			},
			{
				name: "cp_amm_position",
				writable: true
			},
			{
				name: "cp_amm_token_a_vault",
				writable: true
			},
			{
				name: "cp_amm_token_b_vault",
				writable: true
			},
			{
				name: "cp_amm_position_nft_account"
			},
			{
				name: "cp_amm_event_authority"
			},
			{
				name: "cp_amm_program",
				address: "cpamdpZCGKUy5JxQXB4dcpGPiikHawvSWAd6mEn1sGG"
			},
			{
				name: "event_authority",
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								95,
								95,
								101,
								118,
								101,
								110,
								116,
								95,
								97,
								117,
								116,
								104,
								111,
								114,
								105,
								116,
								121
							]
						}
					]
				}
			},
			{
				name: "program"
			}
		],
		args: [
			{
				name: "parameters",
				type: {
					defined: {
						name: "ClaimCpAmmPoolParameters"
					}
				}
			}
		]
	},
	{
		name: "claim_creator",
		discriminator: [
			231,
			240,
			197,
			249,
			244,
			10,
			21,
			59
		],
		accounts: [
			{
				name: "payer",
				writable: true,
				signer: true
			},
			{
				name: "pool_authority",
				address: "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB"
			},
			{
				name: "config",
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								99,
								111,
								110,
								102,
								105,
								103
							]
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "pool",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								112,
								111,
								111,
								108
							]
						},
						{
							kind: "account",
							path: "base_mint"
						},
						{
							kind: "account",
							path: "quote_mint"
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "base_mint",
				writable: true
			},
			{
				name: "quote_mint"
			},
			{
				name: "quote_vault",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								113,
								117,
								111,
								116,
								101,
								95,
								118,
								97,
								117,
								108,
								116
							]
						},
						{
							kind: "account",
							path: "config"
						},
						{
							kind: "account",
							path: "quote_mint"
						}
					]
				}
			},
			{
				name: "token_account",
				docs: [
					"The user token account for output token"
				],
				writable: true
			},
			{
				name: "token_base_program"
			},
			{
				name: "token_quote_program"
			},
			{
				name: "event_authority",
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								95,
								95,
								101,
								118,
								101,
								110,
								116,
								95,
								97,
								117,
								116,
								104,
								111,
								114,
								105,
								116,
								121
							]
						}
					]
				}
			},
			{
				name: "program"
			}
		],
		args: [
		]
	},
	{
		name: "claim_prize",
		discriminator: [
			157,
			233,
			139,
			121,
			246,
			62,
			234,
			235
		],
		accounts: [
			{
				name: "payer",
				writable: true,
				signer: true
			},
			{
				name: "pool_authority",
				address: "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB"
			},
			{
				name: "config",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								99,
								111,
								110,
								102,
								105,
								103
							]
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "quote_mint"
			},
			{
				name: "quote_vault",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								113,
								117,
								111,
								116,
								101,
								95,
								118,
								97,
								117,
								108,
								116
							]
						},
						{
							kind: "account",
							path: "config"
						},
						{
							kind: "account",
							path: "quote_mint"
						}
					]
				}
			},
			{
				name: "token_account",
				docs: [
					"The user token account for output token"
				],
				writable: true
			},
			{
				name: "token_quote_program"
			},
			{
				name: "event_authority",
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								95,
								95,
								101,
								118,
								101,
								110,
								116,
								95,
								97,
								117,
								116,
								104,
								111,
								114,
								105,
								116,
								121
							]
						}
					]
				}
			},
			{
				name: "program"
			}
		],
		args: [
		]
	},
	{
		name: "claim_protocol",
		discriminator: [
			230,
			39,
			79,
			248,
			193,
			76,
			247,
			53
		],
		accounts: [
			{
				name: "payer",
				writable: true,
				signer: true
			},
			{
				name: "pool_authority",
				address: "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB"
			},
			{
				name: "config",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								99,
								111,
								110,
								102,
								105,
								103
							]
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "quote_mint"
			},
			{
				name: "quote_vault",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								113,
								117,
								111,
								116,
								101,
								95,
								118,
								97,
								117,
								108,
								116
							]
						},
						{
							kind: "account",
							path: "config"
						},
						{
							kind: "account",
							path: "quote_mint"
						}
					]
				}
			},
			{
				name: "token_account",
				docs: [
					"The user token account for output token"
				],
				writable: true
			},
			{
				name: "token_quote_program"
			},
			{
				name: "event_authority",
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								95,
								95,
								101,
								118,
								101,
								110,
								116,
								95,
								97,
								117,
								116,
								104,
								111,
								114,
								105,
								116,
								121
							]
						}
					]
				}
			},
			{
				name: "program"
			}
		],
		args: [
		]
	},
	{
		name: "claim_user_token",
		discriminator: [
			164,
			41,
			212,
			48,
			37,
			95,
			41,
			109
		],
		accounts: [
			{
				name: "payer",
				writable: true,
				signer: true
			},
			{
				name: "pool_authority",
				address: "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB"
			},
			{
				name: "base_mint",
				writable: true
			},
			{
				name: "quote_mint"
			},
			{
				name: "pool",
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								112,
								111,
								111,
								108
							]
						},
						{
							kind: "account",
							path: "base_mint"
						},
						{
							kind: "account",
							path: "quote_mint"
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "input_token_account",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								117,
								115,
								101,
								114,
								95,
								116,
								111,
								107,
								101,
								110,
								95,
								97,
								99,
								99,
								111,
								117,
								110,
								116
							]
						},
						{
							kind: "account",
							path: "base_mint"
						},
						{
							kind: "account",
							path: "payer"
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "output_token_account",
				docs: [
					"The user token account for output token"
				],
				writable: true
			},
			{
				name: "token_base_program"
			},
			{
				name: "token_quote_program"
			},
			{
				name: "event_authority",
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								95,
								95,
								101,
								118,
								101,
								110,
								116,
								95,
								97,
								117,
								116,
								104,
								111,
								114,
								105,
								116,
								121
							]
						}
					]
				}
			},
			{
				name: "program"
			}
		],
		args: [
		]
	},
	{
		name: "claim_user_token1",
		discriminator: [
			163,
			250,
			62,
			164,
			192,
			163,
			227,
			147
		],
		accounts: [
			{
				name: "payer",
				writable: true,
				signer: true
			},
			{
				name: "pool_authority",
				address: "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB"
			},
			{
				name: "base_mint",
				writable: true
			},
			{
				name: "quote_mint"
			},
			{
				name: "pool",
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								112,
								111,
								111,
								108
							]
						},
						{
							kind: "account",
							path: "base_mint"
						},
						{
							kind: "account",
							path: "quote_mint"
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "input_token_account",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								117,
								115,
								101,
								114,
								95,
								116,
								111,
								107,
								101,
								110,
								95,
								97,
								99,
								99,
								111,
								117,
								110,
								116
							]
						},
						{
							kind: "account",
							path: "base_mint"
						},
						{
							kind: "account",
							path: "owner"
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "output_token_account",
				docs: [
					"The user token account for output token"
				],
				writable: true
			},
			{
				name: "owner"
			},
			{
				name: "token_base_program"
			},
			{
				name: "token_quote_program"
			},
			{
				name: "event_authority",
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								95,
								95,
								101,
								118,
								101,
								110,
								116,
								95,
								97,
								117,
								116,
								104,
								111,
								114,
								105,
								116,
								121
							]
						}
					]
				}
			},
			{
				name: "program"
			}
		],
		args: [
		]
	},
	{
		name: "initialize_config",
		discriminator: [
			208,
			127,
			21,
			1,
			194,
			190,
			196,
			70
		],
		accounts: [
			{
				name: "pool_authority",
				address: "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB"
			},
			{
				name: "config",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								99,
								111,
								110,
								102,
								105,
								103
							]
						}
					]
				}
			},
			{
				name: "quote_mint"
			},
			{
				name: "quote_vault",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								113,
								117,
								111,
								116,
								101,
								95,
								118,
								97,
								117,
								108,
								116
							]
						},
						{
							kind: "account",
							path: "config"
						},
						{
							kind: "account",
							path: "quote_mint"
						}
					]
				}
			},
			{
				name: "payer",
				writable: true,
				signer: true
			},
			{
				name: "token_quote_program",
				docs: [
					"Program to create mint account and mint tokens"
				]
			},
			{
				name: "system_program",
				address: "11111111111111111111111111111111"
			}
		],
		args: [
		]
	},
	{
		name: "initialize_spl_pool",
		discriminator: [
			220,
			77,
			162,
			14,
			209,
			171,
			12,
			200
		],
		accounts: [
			{
				name: "pool_authority",
				address: "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB"
			},
			{
				name: "config",
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								99,
								111,
								110,
								102,
								105,
								103
							]
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "base_mint",
				writable: true,
				signer: true
			},
			{
				name: "quote_mint"
			},
			{
				name: "pool",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								112,
								111,
								111,
								108
							]
						},
						{
							kind: "account",
							path: "base_mint"
						},
						{
							kind: "account",
							path: "quote_mint"
						}
					]
				}
			},
			{
				name: "base_vault",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								98,
								97,
								115,
								101,
								95,
								118,
								97,
								117,
								108,
								116
							]
						},
						{
							kind: "account",
							path: "config"
						},
						{
							kind: "account",
							path: "base_mint"
						}
					]
				}
			},
			{
				name: "quote_vault",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								113,
								117,
								111,
								116,
								101,
								95,
								118,
								97,
								117,
								108,
								116
							]
						},
						{
							kind: "account",
							path: "config"
						},
						{
							kind: "account",
							path: "quote_mint"
						}
					]
				}
			},
			{
				name: "mint_metadata",
				writable: true
			},
			{
				name: "metadata_program",
				address: "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"
			},
			{
				name: "payer",
				writable: true,
				signer: true
			},
			{
				name: "token_base_program"
			},
			{
				name: "token_quote_program"
			},
			{
				name: "system_program",
				address: "11111111111111111111111111111111"
			},
			{
				name: "event_authority",
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								95,
								95,
								101,
								118,
								101,
								110,
								116,
								95,
								97,
								117,
								116,
								104,
								111,
								114,
								105,
								116,
								121
							]
						}
					]
				}
			},
			{
				name: "program"
			}
		],
		args: [
			{
				name: "parameters",
				type: {
					defined: {
						name: "InitializePoolParameters"
					}
				}
			}
		]
	},
	{
		name: "migration_token",
		discriminator: [
			29,
			61,
			122,
			95,
			208,
			221,
			166,
			184
		],
		accounts: [
			{
				name: "payer",
				writable: true,
				signer: true
			},
			{
				name: "pool_authority",
				writable: true,
				address: "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB"
			},
			{
				name: "config",
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								99,
								111,
								110,
								102,
								105,
								103
							]
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "base_mint",
				writable: true
			},
			{
				name: "quote_mint"
			},
			{
				name: "pool",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								112,
								111,
								111,
								108
							]
						},
						{
							kind: "account",
							path: "base_mint"
						},
						{
							kind: "account",
							path: "quote_mint"
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "base_vault",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								98,
								97,
								115,
								101,
								95,
								118,
								97,
								117,
								108,
								116
							]
						},
						{
							kind: "account",
							path: "config"
						},
						{
							kind: "account",
							path: "base_mint"
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "quote_vault",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								113,
								117,
								111,
								116,
								101,
								95,
								118,
								97,
								117,
								108,
								116
							]
						},
						{
							kind: "account",
							path: "config"
						},
						{
							kind: "account",
							path: "quote_mint"
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "token_quote_program"
			},
			{
				name: "token_base_program"
			},
			{
				name: "system_program",
				address: "11111111111111111111111111111111"
			},
			{
				name: "cp_amm_position_nft_mint",
				docs: [
					"meteora"
				],
				writable: true,
				signer: true
			},
			{
				name: "cp_amm_position_nft_account",
				writable: true
			},
			{
				name: "cp_amm_pool_authority"
			},
			{
				name: "cp_amm_pool",
				writable: true
			},
			{
				name: "cp_amm_position",
				writable: true
			},
			{
				name: "cp_amm_token_a_vault",
				writable: true
			},
			{
				name: "cp_amm_token_b_vault",
				writable: true
			},
			{
				name: "token_2022_program",
				address: "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"
			},
			{
				name: "cp_amm_event_authority"
			},
			{
				name: "cp_amm_program",
				address: "cpamdpZCGKUy5JxQXB4dcpGPiikHawvSWAd6mEn1sGG"
			},
			{
				name: "event_authority",
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								95,
								95,
								101,
								118,
								101,
								110,
								116,
								95,
								97,
								117,
								116,
								104,
								111,
								114,
								105,
								116,
								121
							]
						}
					]
				}
			},
			{
				name: "program"
			}
		],
		args: [
			{
				name: "parameters",
				type: {
					defined: {
						name: "MigrationTokenParameters"
					}
				}
			}
		]
	},
	{
		name: "refund_token",
		discriminator: [
			198,
			194,
			93,
			209,
			12,
			211,
			46,
			174
		],
		accounts: [
			{
				name: "payer",
				writable: true,
				signer: true
			},
			{
				name: "pool_authority",
				address: "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB"
			},
			{
				name: "config",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								99,
								111,
								110,
								102,
								105,
								103
							]
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "base_mint",
				writable: true
			},
			{
				name: "quote_mint"
			},
			{
				name: "pool",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								112,
								111,
								111,
								108
							]
						},
						{
							kind: "account",
							path: "base_mint"
						},
						{
							kind: "account",
							path: "quote_mint"
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "base_vault",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								98,
								97,
								115,
								101,
								95,
								118,
								97,
								117,
								108,
								116
							]
						},
						{
							kind: "account",
							path: "config"
						},
						{
							kind: "account",
							path: "base_mint"
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "quote_vault",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								113,
								117,
								111,
								116,
								101,
								95,
								118,
								97,
								117,
								108,
								116
							]
						},
						{
							kind: "account",
							path: "config"
						},
						{
							kind: "account",
							path: "quote_mint"
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "input_token_account",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								117,
								115,
								101,
								114,
								95,
								116,
								111,
								107,
								101,
								110,
								95,
								97,
								99,
								99,
								111,
								117,
								110,
								116
							]
						},
						{
							kind: "account",
							path: "base_mint"
						},
						{
							kind: "account",
							path: "payer"
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "output_token_account",
				writable: true
			},
			{
				name: "token_quote_program"
			},
			{
				name: "token_base_program"
			},
			{
				name: "system_program",
				address: "11111111111111111111111111111111"
			},
			{
				name: "event_authority",
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								95,
								95,
								101,
								118,
								101,
								110,
								116,
								95,
								97,
								117,
								116,
								104,
								111,
								114,
								105,
								116,
								121
							]
						}
					]
				}
			},
			{
				name: "program"
			}
		],
		args: [
		]
	},
	{
		name: "refund_token1",
		discriminator: [
			139,
			18,
			167,
			208,
			174,
			17,
			74,
			73
		],
		accounts: [
			{
				name: "payer",
				writable: true,
				signer: true
			},
			{
				name: "pool_authority",
				address: "DX9x1skNyCBRsY6foxJ566ASJPdjcHmci43Xh3yw36HB"
			},
			{
				name: "config",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								99,
								111,
								110,
								102,
								105,
								103
							]
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "base_mint",
				writable: true
			},
			{
				name: "quote_mint"
			},
			{
				name: "pool",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								112,
								111,
								111,
								108
							]
						},
						{
							kind: "account",
							path: "base_mint"
						},
						{
							kind: "account",
							path: "quote_mint"
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "base_vault",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								98,
								97,
								115,
								101,
								95,
								118,
								97,
								117,
								108,
								116
							]
						},
						{
							kind: "account",
							path: "config"
						},
						{
							kind: "account",
							path: "base_mint"
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "quote_vault",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								113,
								117,
								111,
								116,
								101,
								95,
								118,
								97,
								117,
								108,
								116
							]
						},
						{
							kind: "account",
							path: "config"
						},
						{
							kind: "account",
							path: "quote_mint"
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "input_token_account",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								117,
								115,
								101,
								114,
								95,
								116,
								111,
								107,
								101,
								110,
								95,
								97,
								99,
								99,
								111,
								117,
								110,
								116
							]
						},
						{
							kind: "account",
							path: "base_mint"
						},
						{
							kind: "account",
							path: "owner"
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			},
			{
				name: "output_token_account",
				writable: true
			},
			{
				name: "owner"
			},
			{
				name: "token_quote_program"
			},
			{
				name: "token_base_program"
			},
			{
				name: "system_program",
				address: "11111111111111111111111111111111"
			},
			{
				name: "event_authority",
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								95,
								95,
								101,
								118,
								101,
								110,
								116,
								95,
								97,
								117,
								116,
								104,
								111,
								114,
								105,
								116,
								121
							]
						}
					]
				}
			},
			{
				name: "program"
			}
		],
		args: [
		]
	},
	{
		name: "set_fee",
		discriminator: [
			18,
			154,
			24,
			18,
			237,
			214,
			19,
			80
		],
		accounts: [
			{
				name: "payer",
				writable: true,
				signer: true
			},
			{
				name: "config",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								99,
								111,
								110,
								102,
								105,
								103
							]
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			}
		],
		args: [
			{
				name: "parameters",
				type: {
					defined: {
						name: "SetFeeParameters"
					}
				}
			}
		]
	},
	{
		name: "set_is_open",
		discriminator: [
			18,
			178,
			20,
			101,
			216,
			109,
			120,
			91
		],
		accounts: [
			{
				name: "payer",
				writable: true,
				signer: true
			},
			{
				name: "config",
				writable: true,
				pda: {
					seeds: [
						{
							kind: "const",
							value: [
								99,
								111,
								110,
								102,
								105,
								103
							]
						}
					],
					program: {
						kind: "const",
						value: [
							254,
							106,
							54,
							177,
							90,
							171,
							158,
							137,
							49,
							48,
							101,
							188,
							131,
							121,
							2,
							228,
							234,
							190,
							158,
							169,
							183,
							92,
							174,
							94,
							103,
							171,
							130,
							147,
							18,
							20,
							41,
							114
						]
					}
				}
			}
		],
		args: [
			{
				name: "parameters",
				type: {
					defined: {
						name: "SetIsOpenParameters"
					}
				}
			}
		]
	}
];
var accounts = [
	{
		name: "Config",
		discriminator: [
			155,
			12,
			170,
			224,
			30,
			250,
			204,
			130
		]
	},
	{
		name: "PoolConfig",
		discriminator: [
			26,
			108,
			14,
			123,
			116,
			230,
			129,
			43
		]
	}
];
var events = [
	{
		name: "EvtBuy",
		discriminator: [
			17,
			72,
			229,
			72,
			199,
			251,
			146,
			52
		]
	},
	{
		name: "EvtComplete",
		discriminator: [
			226,
			27,
			174,
			149,
			122,
			226,
			53,
			26
		]
	},
	{
		name: "EvtCreate",
		discriminator: [
			161,
			151,
			143,
			156,
			214,
			22,
			51,
			176
		]
	},
	{
		name: "EvtIncomplete",
		discriminator: [
			220,
			102,
			179,
			92,
			97,
			70,
			196,
			230
		]
	},
	{
		name: "EvtLiquidityAdded",
		discriminator: [
			179,
			26,
			205,
			20,
			216,
			117,
			57,
			101
		]
	},
	{
		name: "EvtRefund",
		discriminator: [
			117,
			182,
			71,
			97,
			117,
			66,
			212,
			43
		]
	}
];
var errors = [
	{
		code: 6000,
		name: "MathOverflow"
	},
	{
		code: 6001,
		name: "InvalidFee"
	},
	{
		code: 6002,
		name: "ExceededSlippage"
	},
	{
		code: 6003,
		name: "PoolDisabled"
	},
	{
		code: 6004,
		name: "ExceedMaxFeeBps"
	},
	{
		code: 6005,
		name: "InvalidAdmin"
	},
	{
		code: 6006,
		name: "AmountIsZero"
	},
	{
		code: 6007,
		name: "TypeCastFailed"
	},
	{
		code: 6008,
		name: "UnableToModifyActivationPoint"
	},
	{
		code: 6009,
		name: "InvalidAuthorityToCreateThePool"
	},
	{
		code: 6010,
		name: "InvalidActivationType"
	},
	{
		code: 6011,
		name: "InvalidActivationPoint"
	},
	{
		code: 6012,
		name: "InvalidQuoteMint"
	},
	{
		code: 6013,
		name: "InvalidFeeCurve"
	},
	{
		code: 6014,
		name: "InvalidPriceRange"
	},
	{
		code: 6015,
		name: "PriceRangeViolation"
	},
	{
		code: 6016,
		name: "InvalidParameters"
	},
	{
		code: 6017,
		name: "InvalidCollectFeeMode"
	},
	{
		code: 6018,
		name: "InvalidInput"
	},
	{
		code: 6019,
		name: "CannotCreateTokenBadgeOnSupportedMint"
	},
	{
		code: 6020,
		name: "InvalidTokenBadge"
	},
	{
		code: 6021,
		name: "InvalidMinimumLiquidity"
	},
	{
		code: 6022,
		name: "InvalidVestingInfo"
	},
	{
		code: 6023,
		name: "InsufficientLiquidity"
	},
	{
		code: 6024,
		name: "InvalidVestingAccount"
	},
	{
		code: 6025,
		name: "InvalidPoolStatus"
	},
	{
		code: 6026,
		name: "UnsupportNativeMintToken2022"
	},
	{
		code: 6027,
		name: "InvalidRewardIndex"
	},
	{
		code: 6028,
		name: "InvalidRewardDuration"
	},
	{
		code: 6029,
		name: "RewardInitialized"
	},
	{
		code: 6030,
		name: "RewardUninitialized"
	},
	{
		code: 6031,
		name: "InvalidRewardVault"
	},
	{
		code: 6032,
		name: "MustWithdrawnIneligibleReward"
	},
	{
		code: 6033,
		name: "IdenticalRewardDuration"
	},
	{
		code: 6034,
		name: "RewardCampaignInProgress"
	},
	{
		code: 6035,
		name: "IdenticalFunder"
	},
	{
		code: 6036,
		name: "InvalidFunder"
	},
	{
		code: 6037,
		name: "RewardNotEnded"
	},
	{
		code: 6038,
		name: "FeeInverseIsIncorrect"
	},
	{
		code: 6039,
		name: "PositionIsNotEmpty"
	},
	{
		code: 6040,
		name: "InvalidPoolCreatorAuthority"
	},
	{
		code: 6041,
		name: "InvalidConfigType"
	},
	{
		code: 6042,
		name: "InvalidPoolCreator"
	},
	{
		code: 6043,
		name: "RewardVaultFrozenSkipRequired"
	},
	{
		code: 6044,
		name: "InvalidSplitPositionParameters"
	},
	{
		code: 6045,
		name: "UnsupportPositionHasVestingLock"
	},
	{
		code: 6046,
		name: "SamePosition"
	},
	{
		code: 6047,
		name: "InvalidBaseFeeMode"
	},
	{
		code: 6048,
		name: "InvalidFeeRateLimiter"
	},
	{
		code: 6049,
		name: "FailToValidateSingleSwapInstruction"
	},
	{
		code: 6050,
		name: "InvalidFeeTimeScheduler"
	},
	{
		code: 6051,
		name: "UndeterminedError"
	},
	{
		code: 6052,
		name: "InvalidPoolVersion"
	},
	{
		code: 6053,
		name: "InvalidAuthority"
	},
	{
		code: 6054,
		name: "InvalidPermission"
	},
	{
		code: 6055,
		name: "InvalidFeeMarketCapScheduler"
	},
	{
		code: 6056,
		name: "CannotUpdateBaseFee"
	},
	{
		code: 6057,
		name: "InvalidDynamicFeeParameters"
	},
	{
		code: 6058,
		name: "InvalidUpdatePoolFeesParameters"
	},
	{
		code: 6059,
		name: "MissingOperatorAccount"
	},
	{
		code: 6060,
		name: "IncorrectATA"
	},
	{
		code: 6061,
		name: "InvalidZapOutParameters"
	},
	{
		code: 6062,
		name: "InvalidWithdrawProtocolFeeZapAccounts"
	},
	{
		code: 6063,
		name: "MintRestrictedFromZap"
	},
	{
		code: 6064,
		name: "CpiDisabled"
	},
	{
		code: 6065,
		name: "MissingZapOutInstruction"
	},
	{
		code: 6066,
		name: "InvalidZapAccounts"
	},
	{
		code: 6067,
		name: "InvalidCompoundingFeeBps"
	}
];
var types = [
	{
		name: "BaseFeeParameters",
		type: {
			kind: "struct",
			fields: [
				{
					name: "data",
					type: {
						array: [
							"u8",
							27
						]
					}
				}
			]
		}
	},
	{
		name: "BuyTokenParameters",
		type: {
			kind: "struct",
			fields: [
				{
					name: "copies",
					type: "u64"
				}
			]
		}
	},
	{
		name: "ClaimCpAmmPoolParameters",
		type: {
			kind: "struct",
			fields: [
				{
					name: "amount",
					type: "u64"
				}
			]
		}
	},
	{
		name: "Config",
		serialization: "bytemuck",
		repr: {
			kind: "c"
		},
		type: {
			kind: "struct",
			fields: [
				{
					name: "is_open",
					type: "u8"
				},
				{
					name: "_padding0",
					type: {
						array: [
							"u8",
							7
						]
					}
				},
				{
					name: "quote_mint",
					type: "pubkey"
				},
				{
					name: "quote_vault",
					type: "pubkey"
				},
				{
					name: "base_token_decimal",
					type: "u8"
				},
				{
					name: "_padding1",
					type: {
						array: [
							"u8",
							3
						]
					}
				},
				{
					name: "protocol_fee_bps",
					type: "u16"
				},
				{
					name: "_padding2",
					type: {
						array: [
							"u8",
							2
						]
					}
				},
				{
					name: "creator_fee_bps",
					type: "u16"
				},
				{
					name: "_padding3",
					type: {
						array: [
							"u8",
							2
						]
					}
				},
				{
					name: "prize_fee_bps",
					type: "u16"
				},
				{
					name: "_padding4",
					type: {
						array: [
							"u8",
							2
						]
					}
				},
				{
					name: "pass_threshold",
					type: "u64"
				},
				{
					name: "migration_threshold",
					type: "u64"
				},
				{
					name: "protocol_fee",
					type: "u64"
				},
				{
					name: "prize_pool_fee",
					type: "u64"
				}
			]
		}
	},
	{
		name: "DynamicFeeParameters",
		type: {
			kind: "struct",
			fields: [
				{
					name: "bin_step",
					type: "u16"
				},
				{
					name: "bin_step_u128",
					type: "u128"
				},
				{
					name: "filter_period",
					type: "u16"
				},
				{
					name: "decay_period",
					type: "u16"
				},
				{
					name: "reduction_factor",
					type: "u16"
				},
				{
					name: "max_volatility_accumulator",
					type: "u32"
				},
				{
					name: "variable_fee_control",
					type: "u32"
				}
			]
		}
	},
	{
		name: "EvtBuy",
		type: {
			kind: "struct",
			fields: [
				{
					name: "buyer",
					type: "pubkey"
				},
				{
					name: "pool",
					type: "pubkey"
				},
				{
					name: "base_mint",
					type: "pubkey"
				},
				{
					name: "quote_mint",
					type: "pubkey"
				},
				{
					name: "migration_base_threshold",
					type: "u64"
				},
				{
					name: "migration_threshold",
					type: "u64"
				},
				{
					name: "current_timestamp",
					type: "i64"
				},
				{
					name: "copies",
					type: "u64"
				}
			]
		}
	},
	{
		name: "EvtComplete",
		type: {
			kind: "struct",
			fields: [
				{
					name: "pool",
					type: "pubkey"
				},
				{
					name: "base_mint",
					type: "pubkey"
				},
				{
					name: "quote_mint",
					type: "pubkey"
				},
				{
					name: "current_timestamp",
					type: "i64"
				}
			]
		}
	},
	{
		name: "EvtCreate",
		type: {
			kind: "struct",
			fields: [
				{
					name: "pool",
					type: "pubkey"
				},
				{
					name: "base_mint",
					type: "pubkey"
				},
				{
					name: "quote_mint",
					type: "pubkey"
				},
				{
					name: "current_timestamp",
					type: "i64"
				},
				{
					name: "mint_info",
					type: {
						defined: {
							name: "MintData"
						}
					}
				}
			]
		}
	},
	{
		name: "EvtIncomplete",
		type: {
			kind: "struct",
			fields: [
				{
					name: "pool",
					type: "pubkey"
				},
				{
					name: "base_mint",
					type: "pubkey"
				},
				{
					name: "quote_mint",
					type: "pubkey"
				},
				{
					name: "current_timestamp",
					type: "i64"
				}
			]
		}
	},
	{
		name: "EvtLiquidityAdded",
		type: {
			kind: "struct",
			fields: [
				{
					name: "pool",
					type: "pubkey"
				},
				{
					name: "base_mint",
					type: "pubkey"
				},
				{
					name: "quote_mint",
					type: "pubkey"
				},
				{
					name: "current_timestamp",
					type: "i64"
				}
			]
		}
	},
	{
		name: "EvtRefund",
		type: {
			kind: "struct",
			fields: [
				{
					name: "recipient",
					type: "pubkey"
				},
				{
					name: "pool",
					type: "pubkey"
				},
				{
					name: "base_mint",
					type: "pubkey"
				},
				{
					name: "quote_mint",
					type: "pubkey"
				},
				{
					name: "current_timestamp",
					type: "i64"
				}
			]
		}
	},
	{
		name: "InitializePoolParameters",
		type: {
			kind: "struct",
			fields: [
				{
					name: "name",
					type: "string"
				},
				{
					name: "symbol",
					type: "string"
				},
				{
					name: "uri",
					type: "string"
				}
			]
		}
	},
	{
		name: "MigrationTokenParameters",
		type: {
			kind: "struct",
			fields: [
				{
					name: "base_fee",
					type: {
						defined: {
							name: "BaseFeeParameters"
						}
					}
				},
				{
					name: "dynamic_fee",
					type: {
						option: {
							defined: {
								name: "DynamicFeeParameters"
							}
						}
					}
				}
			]
		}
	},
	{
		name: "MintData",
		type: {
			kind: "struct",
			fields: [
				{
					name: "creator",
					type: "pubkey"
				},
				{
					name: "name",
					type: "string"
				},
				{
					name: "symbol",
					type: "string"
				},
				{
					name: "uri",
					type: "string"
				},
				{
					name: "migration_threshold",
					type: "u64"
				}
			]
		}
	},
	{
		name: "PoolConfig",
		serialization: "bytemuck",
		repr: {
			kind: "c"
		},
		type: {
			kind: "struct",
			fields: [
				{
					name: "pool_authority",
					type: "pubkey"
				},
				{
					name: "creator",
					type: "pubkey"
				},
				{
					name: "base_mint",
					type: "pubkey"
				},
				{
					name: "quote_mint",
					type: "pubkey"
				},
				{
					name: "creator_fee",
					type: "u64"
				},
				{
					name: "base_vault",
					type: "pubkey"
				},
				{
					name: "quote_vault",
					type: "pubkey"
				},
				{
					name: "created_at",
					type: "i64"
				},
				{
					name: "migration_base_threshold",
					type: "u64"
				},
				{
					name: "migration_quote_threshold",
					type: "u64"
				},
				{
					name: "pass_threshold",
					type: "u64"
				},
				{
					name: "liquidity_added",
					type: "u8"
				},
				{
					name: "_padding",
					type: {
						array: [
							"u8",
							7
						]
					}
				}
			]
		}
	},
	{
		name: "SetFeeParameters",
		type: {
			kind: "struct",
			fields: [
				{
					name: "protocol_fee_bps",
					type: "u16"
				},
				{
					name: "creator_fee_bps",
					type: "u16"
				},
				{
					name: "prize_fee_bps",
					type: "u16"
				}
			]
		}
	},
	{
		name: "SetIsOpenParameters",
		type: {
			kind: "struct",
			fields: [
				{
					name: "is_open",
					type: "u8"
				}
			]
		}
	}
];
var constants = [
	{
		name: "BASE_VAULT_PREFIX",
		type: "bytes",
		value: "[98, 97, 115, 101, 95, 118, 97, 117, 108, 116]"
	},
	{
		name: "CONFIG_PREFIX",
		type: "bytes",
		value: "[99, 111, 110, 102, 105, 103]"
	},
	{
		name: "POOL_AUTHORITY_PREFIX",
		type: "bytes",
		value: "[112, 111, 111, 108, 95, 97, 117, 116, 104, 111, 114, 105, 116, 121]"
	},
	{
		name: "POOL_PREFIX",
		type: "bytes",
		value: "[112, 111, 111, 108]"
	},
	{
		name: "PRIZE_POOL_VAULT_PREFIX",
		type: "bytes",
		value: "[112, 114, 105, 122, 101, 95, 112, 111, 111, 108, 95, 118, 97, 117, 108, 116]"
	},
	{
		name: "PROTOCOL_VAULT_PREFIX",
		type: "bytes",
		value: "[112, 114, 111, 116, 111, 99, 111, 108, 95, 102, 101, 101, 95, 118, 97, 117, 108, 116]"
	},
	{
		name: "QUOTE_VAULT_PREFIX",
		type: "bytes",
		value: "[113, 117, 111, 116, 101, 95, 118, 97, 117, 108, 116]"
	},
	{
		name: "USER_TOKEN_ACCOUNT_PREFIX",
		type: "bytes",
		value: "[117, 115, 101, 114, 95, 116, 111, 107, 101, 110, 95, 97, 99, 99, 111, 117, 110, 116]"
	}
];
var idl = {
	address: address,
	metadata: metadata,
	instructions: instructions,
	accounts: accounts,
	events: events,
	errors: errors,
	types: types,
	constants: constants
};

export { type BuyTokenAccounts, type BuyTokenParameters, CLAWLAB_PROGRAM_ID, type ClaimFeeParams, type ClaimTokenParams, ClawlabClient, idl as ClawlabIdl, ClawlabProgram, type Clawlab as ClawlabTypes, type Config, type CreateParams, CreatorService, DAMM_V2_PROGRAM_ID, type InitializePoolParameters, METAPLEX_PROGRAM_ID, type MintToParams, type PoolConfig, PoolService, type RefundParams, StateService, UserService, createClawlabProgram, createDammV2Program, deriveBaseVault, deriveConfig, deriveEventAuthority, deriveMintMetadata, derivePool, derivePoolAuthority, deriveQuoteVault, deriveUserTokenAccount, findAssociatedTokenAddress, getAccountCreationTimestamp, getAccountCreationTimestamps, getAccountData, getOrCreateATAInstruction, getTotalTokenSupply, unwrapSOLInstruction, wrapSOLInstruction };
