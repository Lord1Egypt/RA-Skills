'use strict';

var web3_js = require('@solana/web3.js');
var splToken = require('@solana/spl-token');
var anchor = require('@coral-xyz/anchor');
var BN = require('bn.js');

function _interopDefault (e) { return e && e.__esModule ? e : { default: e }; }

var BN__default = /*#__PURE__*/_interopDefault(BN);

// src/services/creator.ts

// src/idl/clawlab/idl.json
var idl_default = {
  address: "J88VV7gYpBiV2nqt3mUeAwc9hCgB6YoVmqaVAamJRTb7",
  metadata: {
    name: "clawlab",
    version: "0.1.0",
    spec: "0.1.0",
    description: "Created with Anchor"
  },
  instructions: [
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
      args: []
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
      args: []
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
      args: []
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
      args: []
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
      args: []
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
      args: []
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
      args: []
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
      args: []
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
      args: []
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
  ],
  accounts: [
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
  ],
  events: [
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
  ],
  errors: [
    {
      code: 6e3,
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
  ],
  types: [
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
  ],
  constants: [
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
  ]
};

// src/constants.ts
var CLAWLAB_PROGRAM_ID = new web3_js.PublicKey(idl_default.address);
var DAMM_V2_PROGRAM_ID = new web3_js.PublicKey(
  "cpamdpZCGKUy5JxQXB4dcpGPiikHawvSWAd6mEn1sGG"
);
var METAPLEX_PROGRAM_ID = new web3_js.PublicKey(
  "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"
);
async function getAccountData(accountAddress, accountType, program, commitment) {
  const address = accountAddress instanceof web3_js.PublicKey ? accountAddress : new web3_js.PublicKey(accountAddress);
  return await program.account[accountType].fetchNullable(
    address,
    commitment
  );
}
async function getAccountCreationTimestamp(accountAddress, connection) {
  const address = accountAddress instanceof web3_js.PublicKey ? accountAddress : new web3_js.PublicKey(accountAddress);
  const signatures = await connection.getSignaturesForAddress(address, {
    limit: 1
  });
  return signatures[0]?.blockTime ? new Date(signatures[0].blockTime * 1e3) : void 0;
}
async function getAccountCreationTimestamps(accountAddresses, connection) {
  const timestampPromises = accountAddresses.map(
    (address) => getAccountCreationTimestamp(address, connection)
  );
  return Promise.all(timestampPromises);
}
function getTotalTokenSupply(swapBaseAmount, migrationBaseThreshold, lockedVestingParams) {
  try {
    const totalCirculatingAmount = swapBaseAmount.add(
      migrationBaseThreshold
    );
    const totalLockedVestingAmount = lockedVestingParams.cliffUnlockAmount.add(
      lockedVestingParams.amountPerPeriod.mul(
        lockedVestingParams.numberOfPeriod
      )
    );
    const totalAmount = totalCirculatingAmount.add(totalLockedVestingAmount);
    if (totalAmount.isNeg() || totalAmount.bitLength() > 64) {
      throw new Error("Math overflow");
    }
    return totalAmount;
  } catch (error) {
    throw new Error(`Math overflow: ${error}`);
  }
}

// src/idl/damm-v2/idl.json
var idl_default2 = {
  address: "cpamdpZCGKUy5JxQXB4dcpGPiikHawvSWAd6mEn1sGG",
  metadata: {
    name: "cp_amm",
    version: "0.1.7",
    spec: "0.1.0",
    description: "Created with Anchor"
  },
  instructions: [
    {
      name: "add_liquidity",
      discriminator: [
        181,
        157,
        89,
        67,
        143,
        182,
        52,
        72
      ],
      accounts: [
        {
          name: "pool",
          writable: true,
          relations: [
            "position"
          ]
        },
        {
          name: "position",
          writable: true
        },
        {
          name: "token_a_account",
          docs: [
            "The user token a account"
          ],
          writable: true
        },
        {
          name: "token_b_account",
          docs: [
            "The user token b account"
          ],
          writable: true
        },
        {
          name: "token_a_vault",
          docs: [
            "The vault token account for input token"
          ],
          writable: true,
          relations: [
            "pool"
          ]
        },
        {
          name: "token_b_vault",
          docs: [
            "The vault token account for output token"
          ],
          writable: true,
          relations: [
            "pool"
          ]
        },
        {
          name: "token_a_mint",
          docs: [
            "The mint of token a"
          ],
          relations: [
            "pool"
          ]
        },
        {
          name: "token_b_mint",
          docs: [
            "The mint of token b"
          ],
          relations: [
            "pool"
          ]
        },
        {
          name: "position_nft_account",
          docs: [
            "The token account for nft"
          ]
        },
        {
          name: "owner",
          docs: [
            "owner of position"
          ],
          signer: true
        },
        {
          name: "token_a_program",
          docs: [
            "Token a program"
          ]
        },
        {
          name: "token_b_program",
          docs: [
            "Token b program"
          ]
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
          name: "params",
          type: {
            defined: {
              name: "AddLiquidityParameters"
            }
          }
        }
      ]
    },
    {
      name: "claim_partner_fee",
      discriminator: [
        97,
        206,
        39,
        105,
        94,
        94,
        126,
        148
      ],
      accounts: [
        {
          name: "pool_authority",
          address: "HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC"
        },
        {
          name: "pool",
          writable: true
        },
        {
          name: "token_a_account",
          docs: [
            "The treasury token a account"
          ],
          writable: true
        },
        {
          name: "token_b_account",
          docs: [
            "The treasury token b account"
          ],
          writable: true
        },
        {
          name: "token_a_vault",
          docs: [
            "The vault token account for input token"
          ],
          writable: true,
          relations: [
            "pool"
          ]
        },
        {
          name: "token_b_vault",
          docs: [
            "The vault token account for output token"
          ],
          writable: true,
          relations: [
            "pool"
          ]
        },
        {
          name: "token_a_mint",
          docs: [
            "The mint of token a"
          ],
          relations: [
            "pool"
          ]
        },
        {
          name: "token_b_mint",
          docs: [
            "The mint of token b"
          ],
          relations: [
            "pool"
          ]
        },
        {
          name: "partner",
          signer: true,
          relations: [
            "pool"
          ]
        },
        {
          name: "token_a_program",
          docs: [
            "Token a program"
          ]
        },
        {
          name: "token_b_program",
          docs: [
            "Token b program"
          ]
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
          name: "max_amount_a",
          type: "u64"
        },
        {
          name: "max_amount_b",
          type: "u64"
        }
      ]
    },
    {
      name: "claim_position_fee",
      discriminator: [
        180,
        38,
        154,
        17,
        133,
        33,
        162,
        211
      ],
      accounts: [
        {
          name: "pool_authority",
          address: "HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC"
        },
        {
          name: "pool",
          relations: [
            "position"
          ]
        },
        {
          name: "position",
          writable: true
        },
        {
          name: "token_a_account",
          docs: [
            "The user token a account"
          ],
          writable: true
        },
        {
          name: "token_b_account",
          docs: [
            "The user token b account"
          ],
          writable: true
        },
        {
          name: "token_a_vault",
          docs: [
            "The vault token account for input token"
          ],
          writable: true,
          relations: [
            "pool"
          ]
        },
        {
          name: "token_b_vault",
          docs: [
            "The vault token account for output token"
          ],
          writable: true,
          relations: [
            "pool"
          ]
        },
        {
          name: "token_a_mint",
          docs: [
            "The mint of token a"
          ],
          relations: [
            "pool"
          ]
        },
        {
          name: "token_b_mint",
          docs: [
            "The mint of token b"
          ],
          relations: [
            "pool"
          ]
        },
        {
          name: "position_nft_account",
          docs: [
            "The token account for nft"
          ]
        },
        {
          name: "owner",
          docs: [
            "owner of position"
          ],
          signer: true
        },
        {
          name: "token_a_program",
          docs: [
            "Token a program"
          ]
        },
        {
          name: "token_b_program",
          docs: [
            "Token b program"
          ]
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
      args: []
    },
    {
      name: "claim_protocol_fee",
      discriminator: [
        165,
        228,
        133,
        48,
        99,
        249,
        255,
        33
      ],
      accounts: [
        {
          name: "pool_authority",
          address: "HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC"
        },
        {
          name: "pool",
          writable: true
        },
        {
          name: "token_a_vault",
          docs: [
            "The vault token account for input token"
          ],
          writable: true,
          relations: [
            "pool"
          ]
        },
        {
          name: "token_b_vault",
          docs: [
            "The vault token account for output token"
          ],
          writable: true,
          relations: [
            "pool"
          ]
        },
        {
          name: "token_a_mint",
          docs: [
            "The mint of token a"
          ],
          relations: [
            "pool"
          ]
        },
        {
          name: "token_b_mint",
          docs: [
            "The mint of token b"
          ],
          relations: [
            "pool"
          ]
        },
        {
          name: "token_a_account",
          writable: true
        },
        {
          name: "token_b_account",
          writable: true
        },
        {
          name: "operator",
          docs: [
            "Claim fee operator"
          ]
        },
        {
          name: "signer",
          docs: [
            "Operator"
          ],
          signer: true
        },
        {
          name: "token_a_program",
          docs: [
            "Token a program"
          ]
        },
        {
          name: "token_b_program",
          docs: [
            "Token b program"
          ]
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
          name: "max_amount_a",
          type: "u64"
        },
        {
          name: "max_amount_b",
          type: "u64"
        }
      ]
    },
    {
      name: "claim_reward",
      discriminator: [
        149,
        95,
        181,
        242,
        94,
        90,
        158,
        162
      ],
      accounts: [
        {
          name: "pool_authority",
          address: "HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC"
        },
        {
          name: "pool",
          writable: true,
          relations: [
            "position"
          ]
        },
        {
          name: "position",
          writable: true
        },
        {
          name: "reward_vault",
          docs: [
            "The vault token account for reward token"
          ],
          writable: true
        },
        {
          name: "reward_mint"
        },
        {
          name: "user_token_account",
          writable: true
        },
        {
          name: "position_nft_account",
          docs: [
            "The token account for nft"
          ]
        },
        {
          name: "owner",
          docs: [
            "owner of position"
          ],
          signer: true
        },
        {
          name: "token_program"
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
          name: "reward_index",
          type: "u8"
        },
        {
          name: "skip_reward",
          type: "u8"
        }
      ]
    },
    {
      name: "close_config",
      discriminator: [
        145,
        9,
        72,
        157,
        95,
        125,
        61,
        85
      ],
      accounts: [
        {
          name: "config",
          writable: true
        },
        {
          name: "operator"
        },
        {
          name: "signer",
          signer: true
        },
        {
          name: "rent_receiver",
          writable: true
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
      args: []
    },
    {
      name: "close_operator_account",
      discriminator: [
        171,
        9,
        213,
        74,
        120,
        23,
        3,
        29
      ],
      accounts: [
        {
          name: "operator",
          writable: true
        },
        {
          name: "signer",
          signer: true
        },
        {
          name: "rent_receiver",
          writable: true
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
      args: []
    },
    {
      name: "close_position",
      discriminator: [
        123,
        134,
        81,
        0,
        49,
        68,
        98,
        98
      ],
      accounts: [
        {
          name: "position_nft_mint",
          docs: [
            "position_nft_mint"
          ],
          writable: true
        },
        {
          name: "position_nft_account",
          docs: [
            "The token account for nft"
          ],
          writable: true
        },
        {
          name: "pool",
          writable: true,
          relations: [
            "position"
          ]
        },
        {
          name: "position",
          writable: true
        },
        {
          name: "pool_authority",
          address: "HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC"
        },
        {
          name: "rent_receiver",
          writable: true
        },
        {
          name: "owner",
          docs: [
            "Owner of position"
          ],
          signer: true
        },
        {
          name: "token_program",
          docs: [
            "Program to create NFT mint/token account and transfer for token22 account"
          ],
          address: "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"
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
      args: []
    },
    {
      name: "close_token_badge",
      discriminator: [
        108,
        146,
        86,
        110,
        179,
        254,
        10,
        104
      ],
      accounts: [
        {
          name: "token_badge",
          writable: true
        },
        {
          name: "operator"
        },
        {
          name: "signer",
          signer: true
        },
        {
          name: "rent_receiver",
          writable: true
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
      args: []
    },
    {
      name: "create_config",
      docs: [
        "OPERATOR FUNCTIONS /////"
      ],
      discriminator: [
        201,
        207,
        243,
        114,
        75,
        111,
        47,
        189
      ],
      accounts: [
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
              },
              {
                kind: "arg",
                path: "index"
              }
            ]
          }
        },
        {
          name: "operator"
        },
        {
          name: "signer",
          signer: true
        },
        {
          name: "payer",
          writable: true,
          signer: true
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
          name: "index",
          type: "u64"
        },
        {
          name: "config_parameters",
          type: {
            defined: {
              name: "StaticConfigParameters"
            }
          }
        }
      ]
    },
    {
      name: "create_dynamic_config",
      discriminator: [
        81,
        251,
        122,
        78,
        66,
        57,
        208,
        82
      ],
      accounts: [
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
              },
              {
                kind: "arg",
                path: "index"
              }
            ]
          }
        },
        {
          name: "operator"
        },
        {
          name: "signer",
          signer: true
        },
        {
          name: "payer",
          writable: true,
          signer: true
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
          name: "index",
          type: "u64"
        },
        {
          name: "config_parameters",
          type: {
            defined: {
              name: "DynamicConfigParameters"
            }
          }
        }
      ]
    },
    {
      name: "create_operator_account",
      docs: [
        "ADMIN FUNCTIONS /////"
      ],
      discriminator: [
        221,
        64,
        246,
        149,
        240,
        153,
        229,
        163
      ],
      accounts: [
        {
          name: "operator",
          writable: true,
          pda: {
            seeds: [
              {
                kind: "const",
                value: [
                  111,
                  112,
                  101,
                  114,
                  97,
                  116,
                  111,
                  114
                ]
              },
              {
                kind: "account",
                path: "whitelisted_address"
              }
            ]
          }
        },
        {
          name: "whitelisted_address"
        },
        {
          name: "signer",
          signer: true
        },
        {
          name: "payer",
          writable: true,
          signer: true
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
          name: "permission",
          type: "u128"
        }
      ]
    },
    {
      name: "create_position",
      discriminator: [
        48,
        215,
        197,
        153,
        96,
        203,
        180,
        133
      ],
      accounts: [
        {
          name: "owner"
        },
        {
          name: "position_nft_mint",
          docs: [
            "position_nft_mint"
          ],
          writable: true,
          signer: true
        },
        {
          name: "position_nft_account",
          docs: [
            "position nft account"
          ],
          writable: true,
          pda: {
            seeds: [
              {
                kind: "const",
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
                ]
              },
              {
                kind: "account",
                path: "position_nft_mint"
              }
            ]
          }
        },
        {
          name: "pool",
          writable: true
        },
        {
          name: "position",
          writable: true,
          pda: {
            seeds: [
              {
                kind: "const",
                value: [
                  112,
                  111,
                  115,
                  105,
                  116,
                  105,
                  111,
                  110
                ]
              },
              {
                kind: "account",
                path: "position_nft_mint"
              }
            ]
          }
        },
        {
          name: "pool_authority",
          address: "HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC"
        },
        {
          name: "payer",
          docs: [
            "Address paying to create the position. Can be anyone"
          ],
          writable: true,
          signer: true
        },
        {
          name: "token_program",
          docs: [
            "Program to create NFT mint/token account and transfer for token22 account"
          ],
          address: "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"
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
      args: []
    },
    {
      name: "create_token_badge",
      discriminator: [
        88,
        206,
        0,
        91,
        60,
        175,
        151,
        118
      ],
      accounts: [
        {
          name: "token_badge",
          writable: true,
          pda: {
            seeds: [
              {
                kind: "const",
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
                ]
              },
              {
                kind: "account",
                path: "token_mint"
              }
            ]
          }
        },
        {
          name: "token_mint"
        },
        {
          name: "operator"
        },
        {
          name: "signer",
          signer: true
        },
        {
          name: "payer",
          writable: true,
          signer: true
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
      args: []
    },
    {
      name: "dummy_ix",
      discriminator: [
        234,
        95,
        176,
        185,
        7,
        42,
        35,
        159
      ],
      accounts: [
        {
          name: "pod_aligned_fee_time_scheduler"
        },
        {
          name: "pod_aligned_fee_rate_limiter"
        },
        {
          name: "pod_aligned_fee_market_cap_scheduler"
        }
      ],
      args: [
        {
          name: "_ixs",
          type: {
            defined: {
              name: "DummyParams"
            }
          }
        }
      ]
    },
    {
      name: "fund_reward",
      discriminator: [
        188,
        50,
        249,
        165,
        93,
        151,
        38,
        63
      ],
      accounts: [
        {
          name: "pool",
          writable: true
        },
        {
          name: "reward_vault",
          writable: true
        },
        {
          name: "reward_mint"
        },
        {
          name: "funder_token_account",
          writable: true
        },
        {
          name: "funder",
          signer: true
        },
        {
          name: "token_program"
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
          name: "reward_index",
          type: "u8"
        },
        {
          name: "amount",
          type: "u64"
        },
        {
          name: "carry_forward",
          type: "bool"
        }
      ]
    },
    {
      name: "initialize_customizable_pool",
      discriminator: [
        20,
        161,
        241,
        24,
        189,
        221,
        180,
        2
      ],
      accounts: [
        {
          name: "creator"
        },
        {
          name: "position_nft_mint",
          docs: [
            "position_nft_mint"
          ],
          writable: true,
          signer: true
        },
        {
          name: "position_nft_account",
          docs: [
            "position nft account"
          ],
          writable: true,
          pda: {
            seeds: [
              {
                kind: "const",
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
                ]
              },
              {
                kind: "account",
                path: "position_nft_mint"
              }
            ]
          }
        },
        {
          name: "payer",
          docs: [
            "Address paying to create the pool. Can be anyone"
          ],
          writable: true,
          signer: true
        },
        {
          name: "pool_authority",
          address: "HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC"
        },
        {
          name: "pool",
          docs: [
            "Initialize an account to store the pool state"
          ],
          writable: true
        },
        {
          name: "position",
          writable: true,
          pda: {
            seeds: [
              {
                kind: "const",
                value: [
                  112,
                  111,
                  115,
                  105,
                  116,
                  105,
                  111,
                  110
                ]
              },
              {
                kind: "account",
                path: "position_nft_mint"
              }
            ]
          }
        },
        {
          name: "token_a_mint",
          docs: [
            "Token a mint"
          ]
        },
        {
          name: "token_b_mint",
          docs: [
            "Token b mint"
          ]
        },
        {
          name: "token_a_vault",
          docs: [
            "Token a vault for the pool"
          ],
          writable: true,
          pda: {
            seeds: [
              {
                kind: "const",
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
                ]
              },
              {
                kind: "account",
                path: "token_a_mint"
              },
              {
                kind: "account",
                path: "pool"
              }
            ]
          }
        },
        {
          name: "token_b_vault",
          docs: [
            "Token b vault for the pool"
          ],
          writable: true,
          pda: {
            seeds: [
              {
                kind: "const",
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
                ]
              },
              {
                kind: "account",
                path: "token_b_mint"
              },
              {
                kind: "account",
                path: "pool"
              }
            ]
          }
        },
        {
          name: "payer_token_a",
          docs: [
            "payer token a account"
          ],
          writable: true
        },
        {
          name: "payer_token_b",
          docs: [
            "creator token b account"
          ],
          writable: true
        },
        {
          name: "token_a_program",
          docs: [
            "Program to create mint account and mint tokens"
          ]
        },
        {
          name: "token_b_program",
          docs: [
            "Program to create mint account and mint tokens"
          ]
        },
        {
          name: "token_2022_program",
          docs: [
            "Program to create NFT mint/token account and transfer for token22 account"
          ],
          address: "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"
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
          name: "params",
          type: {
            defined: {
              name: "InitializeCustomizablePoolParameters"
            }
          }
        }
      ]
    },
    {
      name: "initialize_pool",
      docs: [
        "USER FUNCTIONS ////"
      ],
      discriminator: [
        95,
        180,
        10,
        172,
        84,
        174,
        232,
        40
      ],
      accounts: [
        {
          name: "creator"
        },
        {
          name: "position_nft_mint",
          docs: [
            "position_nft_mint"
          ],
          writable: true,
          signer: true
        },
        {
          name: "position_nft_account",
          docs: [
            "position nft account"
          ],
          writable: true,
          pda: {
            seeds: [
              {
                kind: "const",
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
                ]
              },
              {
                kind: "account",
                path: "position_nft_mint"
              }
            ]
          }
        },
        {
          name: "payer",
          docs: [
            "Address paying to create the pool. Can be anyone"
          ],
          writable: true,
          signer: true
        },
        {
          name: "config",
          docs: [
            "Which config the pool belongs to."
          ]
        },
        {
          name: "pool_authority",
          address: "HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC"
        },
        {
          name: "pool",
          docs: [
            "Initialize an account to store the pool state"
          ],
          writable: true
        },
        {
          name: "position",
          writable: true,
          pda: {
            seeds: [
              {
                kind: "const",
                value: [
                  112,
                  111,
                  115,
                  105,
                  116,
                  105,
                  111,
                  110
                ]
              },
              {
                kind: "account",
                path: "position_nft_mint"
              }
            ]
          }
        },
        {
          name: "token_a_mint",
          docs: [
            "Token a mint"
          ]
        },
        {
          name: "token_b_mint",
          docs: [
            "Token b mint"
          ]
        },
        {
          name: "token_a_vault",
          docs: [
            "Token a vault for the pool"
          ],
          writable: true,
          pda: {
            seeds: [
              {
                kind: "const",
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
                ]
              },
              {
                kind: "account",
                path: "token_a_mint"
              },
              {
                kind: "account",
                path: "pool"
              }
            ]
          }
        },
        {
          name: "token_b_vault",
          docs: [
            "Token b vault for the pool"
          ],
          writable: true,
          pda: {
            seeds: [
              {
                kind: "const",
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
                ]
              },
              {
                kind: "account",
                path: "token_b_mint"
              },
              {
                kind: "account",
                path: "pool"
              }
            ]
          }
        },
        {
          name: "payer_token_a",
          docs: [
            "payer token a account"
          ],
          writable: true
        },
        {
          name: "payer_token_b",
          docs: [
            "creator token b account"
          ],
          writable: true
        },
        {
          name: "token_a_program",
          docs: [
            "Program to create mint account and mint tokens"
          ]
        },
        {
          name: "token_b_program",
          docs: [
            "Program to create mint account and mint tokens"
          ]
        },
        {
          name: "token_2022_program",
          docs: [
            "Program to create NFT mint/token account and transfer for token22 account"
          ],
          address: "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"
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
          name: "params",
          type: {
            defined: {
              name: "InitializePoolParameters"
            }
          }
        }
      ]
    },
    {
      name: "initialize_pool_with_dynamic_config",
      discriminator: [
        149,
        82,
        72,
        197,
        253,
        252,
        68,
        15
      ],
      accounts: [
        {
          name: "creator"
        },
        {
          name: "position_nft_mint",
          docs: [
            "position_nft_mint"
          ],
          writable: true,
          signer: true
        },
        {
          name: "position_nft_account",
          docs: [
            "position nft account"
          ],
          writable: true,
          pda: {
            seeds: [
              {
                kind: "const",
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
                ]
              },
              {
                kind: "account",
                path: "position_nft_mint"
              }
            ]
          }
        },
        {
          name: "payer",
          docs: [
            "Address paying to create the pool. Can be anyone"
          ],
          writable: true,
          signer: true
        },
        {
          name: "pool_creator_authority",
          signer: true,
          relations: [
            "config"
          ]
        },
        {
          name: "config",
          docs: [
            "Which config the pool belongs to."
          ]
        },
        {
          name: "pool_authority",
          address: "HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC"
        },
        {
          name: "pool",
          docs: [
            "Initialize an account to store the pool state"
          ],
          writable: true
        },
        {
          name: "position",
          writable: true,
          pda: {
            seeds: [
              {
                kind: "const",
                value: [
                  112,
                  111,
                  115,
                  105,
                  116,
                  105,
                  111,
                  110
                ]
              },
              {
                kind: "account",
                path: "position_nft_mint"
              }
            ]
          }
        },
        {
          name: "token_a_mint",
          docs: [
            "Token a mint"
          ]
        },
        {
          name: "token_b_mint",
          docs: [
            "Token b mint"
          ]
        },
        {
          name: "token_a_vault",
          docs: [
            "Token a vault for the pool"
          ],
          writable: true,
          pda: {
            seeds: [
              {
                kind: "const",
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
                ]
              },
              {
                kind: "account",
                path: "token_a_mint"
              },
              {
                kind: "account",
                path: "pool"
              }
            ]
          }
        },
        {
          name: "token_b_vault",
          docs: [
            "Token b vault for the pool"
          ],
          writable: true,
          pda: {
            seeds: [
              {
                kind: "const",
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
                ]
              },
              {
                kind: "account",
                path: "token_b_mint"
              },
              {
                kind: "account",
                path: "pool"
              }
            ]
          }
        },
        {
          name: "payer_token_a",
          docs: [
            "payer token a account"
          ],
          writable: true
        },
        {
          name: "payer_token_b",
          docs: [
            "creator token b account"
          ],
          writable: true
        },
        {
          name: "token_a_program",
          docs: [
            "Program to create mint account and mint tokens"
          ]
        },
        {
          name: "token_b_program",
          docs: [
            "Program to create mint account and mint tokens"
          ]
        },
        {
          name: "token_2022_program",
          docs: [
            "Program to create NFT mint/token account and transfer for token22 account"
          ],
          address: "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"
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
          name: "params",
          type: {
            defined: {
              name: "InitializeCustomizablePoolParameters"
            }
          }
        }
      ]
    },
    {
      name: "initialize_reward",
      discriminator: [
        95,
        135,
        192,
        196,
        242,
        129,
        230,
        68
      ],
      accounts: [
        {
          name: "pool_authority",
          address: "HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC"
        },
        {
          name: "pool",
          writable: true
        },
        {
          name: "reward_vault",
          writable: true,
          pda: {
            seeds: [
              {
                kind: "const",
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
                ]
              },
              {
                kind: "account",
                path: "pool"
              },
              {
                kind: "arg",
                path: "reward_index"
              }
            ]
          }
        },
        {
          name: "reward_mint"
        },
        {
          name: "signer",
          signer: true
        },
        {
          name: "payer",
          writable: true,
          signer: true
        },
        {
          name: "token_program"
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
          name: "reward_index",
          type: "u8"
        },
        {
          name: "reward_duration",
          type: "u64"
        },
        {
          name: "funder",
          type: "pubkey"
        }
      ]
    },
    {
      name: "lock_position",
      discriminator: [
        227,
        62,
        2,
        252,
        247,
        10,
        171,
        185
      ],
      accounts: [
        {
          name: "pool",
          relations: [
            "position"
          ]
        },
        {
          name: "position",
          writable: true
        },
        {
          name: "vesting",
          writable: true,
          signer: true
        },
        {
          name: "position_nft_account",
          docs: [
            "The token account for nft"
          ]
        },
        {
          name: "owner",
          docs: [
            "owner of position"
          ],
          signer: true
        },
        {
          name: "payer",
          writable: true,
          signer: true
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
          name: "params",
          type: {
            defined: {
              name: "VestingParameters"
            }
          }
        }
      ]
    },
    {
      name: "permanent_lock_position",
      discriminator: [
        165,
        176,
        125,
        6,
        231,
        171,
        186,
        213
      ],
      accounts: [
        {
          name: "pool",
          writable: true,
          relations: [
            "position"
          ]
        },
        {
          name: "position",
          writable: true
        },
        {
          name: "position_nft_account",
          docs: [
            "The token account for nft"
          ]
        },
        {
          name: "owner",
          docs: [
            "owner of position"
          ],
          signer: true
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
          name: "permanent_lock_liquidity",
          type: "u128"
        }
      ]
    },
    {
      name: "refresh_vesting",
      discriminator: [
        9,
        94,
        216,
        14,
        116,
        204,
        247,
        0
      ],
      accounts: [
        {
          name: "pool",
          relations: [
            "position"
          ]
        },
        {
          name: "position",
          writable: true
        },
        {
          name: "position_nft_account",
          docs: [
            "The token account for nft"
          ]
        },
        {
          name: "owner"
        }
      ],
      args: []
    },
    {
      name: "remove_all_liquidity",
      discriminator: [
        10,
        51,
        61,
        35,
        112,
        105,
        24,
        85
      ],
      accounts: [
        {
          name: "pool_authority",
          address: "HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC"
        },
        {
          name: "pool",
          writable: true,
          relations: [
            "position"
          ]
        },
        {
          name: "position",
          writable: true
        },
        {
          name: "token_a_account",
          docs: [
            "The user token a account"
          ],
          writable: true
        },
        {
          name: "token_b_account",
          docs: [
            "The user token b account"
          ],
          writable: true
        },
        {
          name: "token_a_vault",
          docs: [
            "The vault token account for input token"
          ],
          writable: true,
          relations: [
            "pool"
          ]
        },
        {
          name: "token_b_vault",
          docs: [
            "The vault token account for output token"
          ],
          writable: true,
          relations: [
            "pool"
          ]
        },
        {
          name: "token_a_mint",
          docs: [
            "The mint of token a"
          ],
          relations: [
            "pool"
          ]
        },
        {
          name: "token_b_mint",
          docs: [
            "The mint of token b"
          ],
          relations: [
            "pool"
          ]
        },
        {
          name: "position_nft_account",
          docs: [
            "The token account for nft"
          ]
        },
        {
          name: "owner",
          docs: [
            "owner of position"
          ],
          signer: true
        },
        {
          name: "token_a_program",
          docs: [
            "Token a program"
          ]
        },
        {
          name: "token_b_program",
          docs: [
            "Token b program"
          ]
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
          name: "token_a_amount_threshold",
          type: "u64"
        },
        {
          name: "token_b_amount_threshold",
          type: "u64"
        }
      ]
    },
    {
      name: "remove_liquidity",
      discriminator: [
        80,
        85,
        209,
        72,
        24,
        206,
        177,
        108
      ],
      accounts: [
        {
          name: "pool_authority",
          address: "HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC"
        },
        {
          name: "pool",
          writable: true,
          relations: [
            "position"
          ]
        },
        {
          name: "position",
          writable: true
        },
        {
          name: "token_a_account",
          docs: [
            "The user token a account"
          ],
          writable: true
        },
        {
          name: "token_b_account",
          docs: [
            "The user token b account"
          ],
          writable: true
        },
        {
          name: "token_a_vault",
          docs: [
            "The vault token account for input token"
          ],
          writable: true,
          relations: [
            "pool"
          ]
        },
        {
          name: "token_b_vault",
          docs: [
            "The vault token account for output token"
          ],
          writable: true,
          relations: [
            "pool"
          ]
        },
        {
          name: "token_a_mint",
          docs: [
            "The mint of token a"
          ],
          relations: [
            "pool"
          ]
        },
        {
          name: "token_b_mint",
          docs: [
            "The mint of token b"
          ],
          relations: [
            "pool"
          ]
        },
        {
          name: "position_nft_account",
          docs: [
            "The token account for nft"
          ]
        },
        {
          name: "owner",
          docs: [
            "owner of position"
          ],
          signer: true
        },
        {
          name: "token_a_program",
          docs: [
            "Token a program"
          ]
        },
        {
          name: "token_b_program",
          docs: [
            "Token b program"
          ]
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
          name: "params",
          type: {
            defined: {
              name: "RemoveLiquidityParameters"
            }
          }
        }
      ]
    },
    {
      name: "set_pool_status",
      discriminator: [
        112,
        87,
        135,
        223,
        83,
        204,
        132,
        53
      ],
      accounts: [
        {
          name: "pool",
          writable: true
        },
        {
          name: "operator"
        },
        {
          name: "signer",
          signer: true
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
          name: "status",
          type: "u8"
        }
      ]
    },
    {
      name: "split_position",
      discriminator: [
        172,
        241,
        221,
        138,
        161,
        29,
        253,
        42
      ],
      accounts: [
        {
          name: "pool",
          writable: true,
          relations: [
            "first_position",
            "second_position"
          ]
        },
        {
          name: "first_position",
          docs: [
            "The first position"
          ],
          writable: true
        },
        {
          name: "first_position_nft_account",
          docs: [
            "The token account for position nft"
          ]
        },
        {
          name: "second_position",
          docs: [
            "The second position"
          ],
          writable: true
        },
        {
          name: "second_position_nft_account",
          docs: [
            "The token account for position nft"
          ]
        },
        {
          name: "first_owner",
          docs: [
            "Owner of first position"
          ],
          signer: true
        },
        {
          name: "second_owner",
          docs: [
            "Owner of second position"
          ],
          signer: true
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
          name: "params",
          type: {
            defined: {
              name: "SplitPositionParameters"
            }
          }
        }
      ]
    },
    {
      name: "split_position2",
      discriminator: [
        221,
        147,
        228,
        207,
        140,
        212,
        17,
        119
      ],
      accounts: [
        {
          name: "pool",
          writable: true,
          relations: [
            "first_position",
            "second_position"
          ]
        },
        {
          name: "first_position",
          docs: [
            "The first position"
          ],
          writable: true
        },
        {
          name: "first_position_nft_account",
          docs: [
            "The token account for position nft"
          ]
        },
        {
          name: "second_position",
          docs: [
            "The second position"
          ],
          writable: true
        },
        {
          name: "second_position_nft_account",
          docs: [
            "The token account for position nft"
          ]
        },
        {
          name: "first_owner",
          docs: [
            "Owner of first position"
          ],
          signer: true
        },
        {
          name: "second_owner",
          docs: [
            "Owner of second position"
          ],
          signer: true
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
          name: "numerator",
          type: "u32"
        }
      ]
    },
    {
      name: "swap",
      discriminator: [
        248,
        198,
        158,
        145,
        225,
        117,
        135,
        200
      ],
      accounts: [
        {
          name: "pool_authority",
          address: "HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC"
        },
        {
          name: "pool",
          docs: [
            "Pool account"
          ],
          writable: true
        },
        {
          name: "input_token_account",
          docs: [
            "The user token account for input token"
          ],
          writable: true
        },
        {
          name: "output_token_account",
          docs: [
            "The user token account for output token"
          ],
          writable: true
        },
        {
          name: "token_a_vault",
          docs: [
            "The vault token account for input token"
          ],
          writable: true,
          relations: [
            "pool"
          ]
        },
        {
          name: "token_b_vault",
          docs: [
            "The vault token account for output token"
          ],
          writable: true,
          relations: [
            "pool"
          ]
        },
        {
          name: "token_a_mint",
          docs: [
            "The mint of token a"
          ]
        },
        {
          name: "token_b_mint",
          docs: [
            "The mint of token b"
          ]
        },
        {
          name: "payer",
          docs: [
            "The user performing the swap"
          ],
          signer: true
        },
        {
          name: "token_a_program",
          docs: [
            "Token a program"
          ]
        },
        {
          name: "token_b_program",
          docs: [
            "Token b program"
          ]
        },
        {
          name: "referral_token_account",
          docs: [
            "referral token account"
          ],
          writable: true,
          optional: true
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
          name: "_params",
          type: {
            defined: {
              name: "SwapParameters"
            }
          }
        }
      ]
    },
    {
      name: "swap2",
      discriminator: [
        65,
        75,
        63,
        76,
        235,
        91,
        91,
        136
      ],
      accounts: [
        {
          name: "pool_authority",
          address: "HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC"
        },
        {
          name: "pool",
          docs: [
            "Pool account"
          ],
          writable: true
        },
        {
          name: "input_token_account",
          docs: [
            "The user token account for input token"
          ],
          writable: true
        },
        {
          name: "output_token_account",
          docs: [
            "The user token account for output token"
          ],
          writable: true
        },
        {
          name: "token_a_vault",
          docs: [
            "The vault token account for input token"
          ],
          writable: true,
          relations: [
            "pool"
          ]
        },
        {
          name: "token_b_vault",
          docs: [
            "The vault token account for output token"
          ],
          writable: true,
          relations: [
            "pool"
          ]
        },
        {
          name: "token_a_mint",
          docs: [
            "The mint of token a"
          ]
        },
        {
          name: "token_b_mint",
          docs: [
            "The mint of token b"
          ]
        },
        {
          name: "payer",
          docs: [
            "The user performing the swap"
          ],
          signer: true
        },
        {
          name: "token_a_program",
          docs: [
            "Token a program"
          ]
        },
        {
          name: "token_b_program",
          docs: [
            "Token b program"
          ]
        },
        {
          name: "referral_token_account",
          docs: [
            "referral token account"
          ],
          writable: true,
          optional: true
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
          name: "_params",
          type: {
            defined: {
              name: "SwapParameters2"
            }
          }
        }
      ]
    },
    {
      name: "update_pool_fees",
      discriminator: [
        118,
        217,
        203,
        179,
        60,
        8,
        70,
        89
      ],
      accounts: [
        {
          name: "pool",
          writable: true
        },
        {
          name: "operator"
        },
        {
          name: "signer",
          signer: true
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
          name: "params",
          type: {
            defined: {
              name: "UpdatePoolFeesParameters"
            }
          }
        }
      ]
    },
    {
      name: "update_reward_duration",
      discriminator: [
        138,
        174,
        196,
        169,
        213,
        235,
        254,
        107
      ],
      accounts: [
        {
          name: "pool",
          writable: true
        },
        {
          name: "signer",
          signer: true
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
          name: "reward_index",
          type: "u8"
        },
        {
          name: "new_duration",
          type: "u64"
        }
      ]
    },
    {
      name: "update_reward_funder",
      discriminator: [
        211,
        28,
        48,
        32,
        215,
        160,
        35,
        23
      ],
      accounts: [
        {
          name: "pool",
          writable: true
        },
        {
          name: "signer",
          signer: true
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
          name: "reward_index",
          type: "u8"
        },
        {
          name: "new_funder",
          type: "pubkey"
        }
      ]
    },
    {
      name: "withdraw_ineligible_reward",
      discriminator: [
        148,
        206,
        42,
        195,
        247,
        49,
        103,
        8
      ],
      accounts: [
        {
          name: "pool_authority",
          address: "HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC"
        },
        {
          name: "pool",
          writable: true
        },
        {
          name: "reward_vault",
          writable: true
        },
        {
          name: "reward_mint"
        },
        {
          name: "funder_token_account",
          writable: true
        },
        {
          name: "funder",
          signer: true
        },
        {
          name: "token_program"
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
          name: "reward_index",
          type: "u8"
        }
      ]
    },
    {
      name: "zap_protocol_fee",
      discriminator: [
        213,
        155,
        187,
        34,
        56,
        182,
        91,
        240
      ],
      accounts: [
        {
          name: "pool_authority",
          address: "HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC"
        },
        {
          name: "pool",
          writable: true
        },
        {
          name: "token_vault",
          writable: true
        },
        {
          name: "token_mint"
        },
        {
          name: "receiver_token",
          writable: true
        },
        {
          name: "operator",
          docs: [
            "zap claim fee operator"
          ]
        },
        {
          name: "signer",
          docs: [
            "Operator"
          ],
          signer: true
        },
        {
          name: "token_program",
          docs: [
            "Token program"
          ]
        },
        {
          name: "sysvar_instructions",
          address: "Sysvar1nstructions1111111111111111111111111"
        }
      ],
      args: [
        {
          name: "max_amount",
          type: "u64"
        }
      ]
    }
  ],
  accounts: [
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
      name: "Operator",
      discriminator: [
        219,
        31,
        188,
        145,
        69,
        139,
        204,
        117
      ]
    },
    {
      name: "PodAlignedFeeMarketCapScheduler",
      discriminator: [
        251,
        130,
        208,
        253,
        245,
        27,
        145,
        203
      ]
    },
    {
      name: "PodAlignedFeeRateLimiter",
      discriminator: [
        160,
        219,
        8,
        251,
        179,
        7,
        16,
        117
      ]
    },
    {
      name: "PodAlignedFeeTimeScheduler",
      discriminator: [
        239,
        132,
        138,
        213,
        67,
        154,
        130,
        70
      ]
    },
    {
      name: "Pool",
      discriminator: [
        241,
        154,
        109,
        4,
        17,
        177,
        109,
        188
      ]
    },
    {
      name: "Position",
      discriminator: [
        170,
        188,
        143,
        228,
        122,
        64,
        247,
        208
      ]
    },
    {
      name: "TokenBadge",
      discriminator: [
        116,
        219,
        204,
        229,
        249,
        116,
        255,
        150
      ]
    },
    {
      name: "Vesting",
      discriminator: [
        100,
        149,
        66,
        138,
        95,
        200,
        128,
        241
      ]
    }
  ],
  events: [
    {
      name: "EvtClaimPartnerFee",
      discriminator: [
        118,
        99,
        77,
        10,
        226,
        1,
        1,
        87
      ]
    },
    {
      name: "EvtClaimPositionFee",
      discriminator: [
        198,
        182,
        183,
        52,
        97,
        12,
        49,
        56
      ]
    },
    {
      name: "EvtClaimProtocolFee",
      discriminator: [
        186,
        244,
        75,
        251,
        188,
        13,
        25,
        33
      ]
    },
    {
      name: "EvtClaimReward",
      discriminator: [
        218,
        86,
        147,
        200,
        235,
        188,
        215,
        231
      ]
    },
    {
      name: "EvtCloseConfig",
      discriminator: [
        36,
        30,
        239,
        45,
        58,
        132,
        14,
        5
      ]
    },
    {
      name: "EvtClosePosition",
      discriminator: [
        20,
        145,
        144,
        68,
        143,
        142,
        214,
        178
      ]
    },
    {
      name: "EvtCreateConfig",
      discriminator: [
        131,
        207,
        180,
        174,
        180,
        73,
        165,
        54
      ]
    },
    {
      name: "EvtCreateDynamicConfig",
      discriminator: [
        231,
        197,
        13,
        164,
        248,
        213,
        133,
        152
      ]
    },
    {
      name: "EvtCreatePosition",
      discriminator: [
        156,
        15,
        119,
        198,
        29,
        181,
        221,
        55
      ]
    },
    {
      name: "EvtCreateTokenBadge",
      discriminator: [
        141,
        120,
        134,
        116,
        34,
        28,
        114,
        160
      ]
    },
    {
      name: "EvtFundReward",
      discriminator: [
        104,
        233,
        237,
        122,
        199,
        191,
        121,
        85
      ]
    },
    {
      name: "EvtInitializePool",
      discriminator: [
        228,
        50,
        246,
        85,
        203,
        66,
        134,
        37
      ]
    },
    {
      name: "EvtInitializeReward",
      discriminator: [
        129,
        91,
        188,
        3,
        246,
        52,
        185,
        249
      ]
    },
    {
      name: "EvtLiquidityChange",
      discriminator: [
        197,
        171,
        78,
        127,
        224,
        211,
        87,
        13
      ]
    },
    {
      name: "EvtLockPosition",
      discriminator: [
        168,
        63,
        108,
        83,
        219,
        82,
        2,
        200
      ]
    },
    {
      name: "EvtPermanentLockPosition",
      discriminator: [
        145,
        143,
        162,
        218,
        218,
        80,
        67,
        11
      ]
    },
    {
      name: "EvtSetPoolStatus",
      discriminator: [
        100,
        213,
        74,
        3,
        95,
        91,
        228,
        146
      ]
    },
    {
      name: "EvtSplitPosition2",
      discriminator: [
        165,
        32,
        203,
        174,
        72,
        100,
        233,
        103
      ]
    },
    {
      name: "EvtSwap2",
      discriminator: [
        189,
        66,
        51,
        168,
        38,
        80,
        117,
        153
      ]
    },
    {
      name: "EvtUpdatePoolFees",
      discriminator: [
        76,
        165,
        246,
        102,
        102,
        217,
        156,
        44
      ]
    },
    {
      name: "EvtUpdateRewardDuration",
      discriminator: [
        149,
        135,
        65,
        231,
        129,
        153,
        65,
        57
      ]
    },
    {
      name: "EvtUpdateRewardFunder",
      discriminator: [
        76,
        154,
        208,
        13,
        40,
        115,
        246,
        146
      ]
    },
    {
      name: "EvtWithdrawIneligibleReward",
      discriminator: [
        248,
        215,
        184,
        78,
        31,
        180,
        179,
        168
      ]
    }
  ],
  errors: [
    {
      code: 6e3,
      name: "MathOverflow",
      msg: "Math operation overflow"
    },
    {
      code: 6001,
      name: "InvalidFee",
      msg: "Invalid fee setup"
    },
    {
      code: 6002,
      name: "ExceededSlippage",
      msg: "Exceeded slippage tolerance"
    },
    {
      code: 6003,
      name: "PoolDisabled",
      msg: "Pool disabled"
    },
    {
      code: 6004,
      name: "ExceedMaxFeeBps",
      msg: "Exceeded max fee bps"
    },
    {
      code: 6005,
      name: "InvalidAdmin",
      msg: "Invalid admin"
    },
    {
      code: 6006,
      name: "AmountIsZero",
      msg: "Amount is zero"
    },
    {
      code: 6007,
      name: "TypeCastFailed",
      msg: "Type cast error"
    },
    {
      code: 6008,
      name: "UnableToModifyActivationPoint",
      msg: "Unable to modify activation point"
    },
    {
      code: 6009,
      name: "InvalidAuthorityToCreateThePool",
      msg: "Invalid authority to create the pool"
    },
    {
      code: 6010,
      name: "InvalidActivationType",
      msg: "Invalid activation type"
    },
    {
      code: 6011,
      name: "InvalidActivationPoint",
      msg: "Invalid activation point"
    },
    {
      code: 6012,
      name: "InvalidQuoteMint",
      msg: "Quote token must be SOL,USDC"
    },
    {
      code: 6013,
      name: "InvalidFeeCurve",
      msg: "Invalid fee curve"
    },
    {
      code: 6014,
      name: "InvalidPriceRange",
      msg: "Invalid Price Range"
    },
    {
      code: 6015,
      name: "PriceRangeViolation",
      msg: "Trade is over price range"
    },
    {
      code: 6016,
      name: "InvalidParameters",
      msg: "Invalid parameters"
    },
    {
      code: 6017,
      name: "InvalidCollectFeeMode",
      msg: "Invalid collect fee mode"
    },
    {
      code: 6018,
      name: "InvalidInput",
      msg: "Invalid input"
    },
    {
      code: 6019,
      name: "CannotCreateTokenBadgeOnSupportedMint",
      msg: "Cannot create token badge on supported mint"
    },
    {
      code: 6020,
      name: "InvalidTokenBadge",
      msg: "Invalid token badge"
    },
    {
      code: 6021,
      name: "InvalidMinimumLiquidity",
      msg: "Invalid minimum liquidity"
    },
    {
      code: 6022,
      name: "InvalidVestingInfo",
      msg: "Invalid vesting information"
    },
    {
      code: 6023,
      name: "InsufficientLiquidity",
      msg: "Insufficient liquidity"
    },
    {
      code: 6024,
      name: "InvalidVestingAccount",
      msg: "Invalid vesting account"
    },
    {
      code: 6025,
      name: "InvalidPoolStatus",
      msg: "Invalid pool status"
    },
    {
      code: 6026,
      name: "UnsupportNativeMintToken2022",
      msg: "Unsupported native mint token2022"
    },
    {
      code: 6027,
      name: "InvalidRewardIndex",
      msg: "Invalid reward index"
    },
    {
      code: 6028,
      name: "InvalidRewardDuration",
      msg: "Invalid reward duration"
    },
    {
      code: 6029,
      name: "RewardInitialized",
      msg: "Reward already initialized"
    },
    {
      code: 6030,
      name: "RewardUninitialized",
      msg: "Reward not initialized"
    },
    {
      code: 6031,
      name: "InvalidRewardVault",
      msg: "Invalid reward vault"
    },
    {
      code: 6032,
      name: "MustWithdrawnIneligibleReward",
      msg: "Must withdraw ineligible reward"
    },
    {
      code: 6033,
      name: "IdenticalRewardDuration",
      msg: "Reward duration is the same"
    },
    {
      code: 6034,
      name: "RewardCampaignInProgress",
      msg: "Reward campaign in progress"
    },
    {
      code: 6035,
      name: "IdenticalFunder",
      msg: "Identical funder"
    },
    {
      code: 6036,
      name: "InvalidFunder",
      msg: "Invalid funder"
    },
    {
      code: 6037,
      name: "RewardNotEnded",
      msg: "Reward not ended"
    },
    {
      code: 6038,
      name: "FeeInverseIsIncorrect",
      msg: "Fee inverse is incorrect"
    },
    {
      code: 6039,
      name: "PositionIsNotEmpty",
      msg: "Position is not empty"
    },
    {
      code: 6040,
      name: "InvalidPoolCreatorAuthority",
      msg: "Invalid pool creator authority"
    },
    {
      code: 6041,
      name: "InvalidConfigType",
      msg: "Invalid config type"
    },
    {
      code: 6042,
      name: "InvalidPoolCreator",
      msg: "Invalid pool creator"
    },
    {
      code: 6043,
      name: "RewardVaultFrozenSkipRequired",
      msg: "Reward vault is frozen, must skip reward to proceed"
    },
    {
      code: 6044,
      name: "InvalidSplitPositionParameters",
      msg: "Invalid parameters for split position"
    },
    {
      code: 6045,
      name: "UnsupportPositionHasVestingLock",
      msg: "Unsupported split position has vesting lock"
    },
    {
      code: 6046,
      name: "SamePosition",
      msg: "Same position"
    },
    {
      code: 6047,
      name: "InvalidBaseFeeMode",
      msg: "Invalid base fee mode"
    },
    {
      code: 6048,
      name: "InvalidFeeRateLimiter",
      msg: "Invalid fee rate limiter"
    },
    {
      code: 6049,
      name: "FailToValidateSingleSwapInstruction",
      msg: "Fail to validate single swap instruction in rate limiter"
    },
    {
      code: 6050,
      name: "InvalidFeeTimeScheduler",
      msg: "Invalid fee scheduler"
    },
    {
      code: 6051,
      name: "UndeterminedError",
      msg: "Undetermined error"
    },
    {
      code: 6052,
      name: "InvalidPoolVersion",
      msg: "Invalid pool version"
    },
    {
      code: 6053,
      name: "InvalidAuthority",
      msg: "Invalid authority to do that action"
    },
    {
      code: 6054,
      name: "InvalidPermission",
      msg: "Invalid permission"
    },
    {
      code: 6055,
      name: "InvalidFeeMarketCapScheduler",
      msg: "Invalid fee market cap scheduler"
    },
    {
      code: 6056,
      name: "CannotUpdateBaseFee",
      msg: "Cannot update base fee"
    },
    {
      code: 6057,
      name: "InvalidDynamicFeeParameters",
      msg: "Invalid dynamic fee parameters"
    },
    {
      code: 6058,
      name: "InvalidUpdatePoolFeesParameters",
      msg: "Invalid update pool fees parameters"
    },
    {
      code: 6059,
      name: "MissingOperatorAccount",
      msg: "Missing operator account"
    },
    {
      code: 6060,
      name: "IncorrectATA",
      msg: "Incorrect ATA"
    },
    {
      code: 6061,
      name: "InvalidZapOutParameters",
      msg: "Invalid zap out parameters"
    },
    {
      code: 6062,
      name: "InvalidWithdrawProtocolFeeZapAccounts",
      msg: "Invalid withdraw protocol fee zap accounts"
    },
    {
      code: 6063,
      name: "MintRestrictedFromZap",
      msg: "SOL,USDC protocol fee cannot be withdrawn via zap"
    },
    {
      code: 6064,
      name: "CpiDisabled",
      msg: "CPI disabled"
    },
    {
      code: 6065,
      name: "MissingZapOutInstruction",
      msg: "Missing zap out instruction"
    },
    {
      code: 6066,
      name: "InvalidZapAccounts",
      msg: "Invalid zap accounts"
    }
  ],
  types: [
    {
      name: "AddLiquidityParameters",
      type: {
        kind: "struct",
        fields: [
          {
            name: "liquidity_delta",
            docs: [
              "delta liquidity"
            ],
            type: "u128"
          },
          {
            name: "token_a_amount_threshold",
            docs: [
              "maximum token a amount"
            ],
            type: "u64"
          },
          {
            name: "token_b_amount_threshold",
            docs: [
              "maximum token b amount"
            ],
            type: "u64"
          }
        ]
      }
    },
    {
      name: "BaseFeeInfo",
      serialization: "bytemuck",
      repr: {
        kind: "c"
      },
      type: {
        kind: "struct",
        fields: [
          {
            name: "data",
            type: {
              array: [
                "u8",
                32
              ]
            }
          }
        ]
      }
    },
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
                30
              ]
            }
          }
        ]
      }
    },
    {
      name: "BaseFeeStruct",
      serialization: "bytemuck",
      repr: {
        kind: "c"
      },
      type: {
        kind: "struct",
        fields: [
          {
            name: "base_fee_info",
            type: {
              defined: {
                name: "BaseFeeInfo"
              }
            }
          },
          {
            name: "padding_1",
            type: "u64"
          }
        ]
      }
    },
    {
      name: "BorshFeeMarketCapScheduler",
      type: {
        kind: "struct",
        fields: [
          {
            name: "cliff_fee_numerator",
            type: "u64"
          },
          {
            name: "number_of_period",
            type: "u16"
          },
          {
            name: "sqrt_price_step_bps",
            type: "u32"
          },
          {
            name: "scheduler_expiration_duration",
            type: "u32"
          },
          {
            name: "reduction_factor",
            type: "u64"
          },
          {
            name: "base_fee_mode",
            type: "u8"
          },
          {
            name: "padding",
            type: {
              array: [
                "u8",
                3
              ]
            }
          }
        ]
      }
    },
    {
      name: "BorshFeeRateLimiter",
      docs: [
        "we denote reference_amount = x0, cliff_fee_numerator = c, fee_increment = i",
        "if input_amount <= x0, then fee = input_amount * c",
        "",
        "if input_amount > x0, then input_amount = x0 + (a * x0 + b)",
        "if a < max_index",
        "then fee = x0 * c + x0 * (c + i) + .... + x0 * (c + i*a) + b * (c + i * (a+1))",
        "then fee = x0 * (c + c*a + i*a*(a+1)/2) + b * (c + i * (a+1))",
        "",
        "if a >= max_index",
        "if a = max_index + d, input_amount = x0 + max_index * x0 + (d * x0 + b)",
        "then fee = x0 * (c + c*max_index + i*max_index*(max_index+1)/2) + (d * x0 + b) * MAX_FEE"
      ],
      type: {
        kind: "struct",
        fields: [
          {
            name: "cliff_fee_numerator",
            type: "u64"
          },
          {
            name: "fee_increment_bps",
            type: "u16"
          },
          {
            name: "max_limiter_duration",
            type: "u32"
          },
          {
            name: "max_fee_bps",
            type: "u32"
          },
          {
            name: "reference_amount",
            type: "u64"
          },
          {
            name: "base_fee_mode",
            type: "u8"
          },
          {
            name: "padding",
            type: {
              array: [
                "u8",
                3
              ]
            }
          }
        ]
      }
    },
    {
      name: "BorshFeeTimeScheduler",
      type: {
        kind: "struct",
        fields: [
          {
            name: "cliff_fee_numerator",
            type: "u64"
          },
          {
            name: "number_of_period",
            type: "u16"
          },
          {
            name: "period_frequency",
            type: "u64"
          },
          {
            name: "reduction_factor",
            type: "u64"
          },
          {
            name: "base_fee_mode",
            type: "u8"
          },
          {
            name: "padding",
            type: {
              array: [
                "u8",
                3
              ]
            }
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
            name: "vault_config_key",
            docs: [
              "Vault config key"
            ],
            type: "pubkey"
          },
          {
            name: "pool_creator_authority",
            docs: [
              "Only pool_creator_authority can use the current config to initialize new pool. When it's Pubkey::default, it's a public config."
            ],
            type: "pubkey"
          },
          {
            name: "pool_fees",
            docs: [
              "Pool fee"
            ],
            type: {
              defined: {
                name: "PoolFeesConfig"
              }
            }
          },
          {
            name: "activation_type",
            docs: [
              "Activation type"
            ],
            type: "u8"
          },
          {
            name: "collect_fee_mode",
            docs: [
              "Collect fee mode"
            ],
            type: "u8"
          },
          {
            name: "config_type",
            docs: [
              "Config type mode, 0 for static, 1 for dynamic"
            ],
            type: "u8"
          },
          {
            name: "_padding_0",
            docs: [
              "padding 0"
            ],
            type: {
              array: [
                "u8",
                5
              ]
            }
          },
          {
            name: "index",
            docs: [
              "config index"
            ],
            type: "u64"
          },
          {
            name: "sqrt_min_price",
            docs: [
              "sqrt min price"
            ],
            type: "u128"
          },
          {
            name: "sqrt_max_price",
            docs: [
              "sqrt max price"
            ],
            type: "u128"
          },
          {
            name: "_padding_1",
            docs: [
              "Fee curve point",
              "Padding for further use"
            ],
            type: {
              array: [
                "u64",
                10
              ]
            }
          }
        ]
      }
    },
    {
      name: "DummyParams",
      type: {
        kind: "struct",
        fields: [
          {
            name: "borsh_fee_time_scheduler_params",
            type: {
              defined: {
                name: "BorshFeeTimeScheduler"
              }
            }
          },
          {
            name: "borsh_fee_rate_limiter_params",
            type: {
              defined: {
                name: "BorshFeeRateLimiter"
              }
            }
          },
          {
            name: "borsh_fee_market_cap_scheduler_params",
            type: {
              defined: {
                name: "BorshFeeMarketCapScheduler"
              }
            }
          }
        ]
      }
    },
    {
      name: "DynamicConfigParameters",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool_creator_authority",
            type: "pubkey"
          }
        ]
      }
    },
    {
      name: "DynamicFeeConfig",
      serialization: "bytemuck",
      repr: {
        kind: "c"
      },
      type: {
        kind: "struct",
        fields: [
          {
            name: "initialized",
            type: "u8"
          },
          {
            name: "padding",
            type: {
              array: [
                "u8",
                7
              ]
            }
          },
          {
            name: "max_volatility_accumulator",
            type: "u32"
          },
          {
            name: "variable_fee_control",
            type: "u32"
          },
          {
            name: "bin_step",
            type: "u16"
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
            name: "padding_1",
            type: {
              array: [
                "u8",
                8
              ]
            }
          },
          {
            name: "bin_step_u128",
            type: "u128"
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
      name: "DynamicFeeStruct",
      serialization: "bytemuck",
      repr: {
        kind: "c"
      },
      type: {
        kind: "struct",
        fields: [
          {
            name: "initialized",
            type: "u8"
          },
          {
            name: "padding",
            type: {
              array: [
                "u8",
                7
              ]
            }
          },
          {
            name: "max_volatility_accumulator",
            type: "u32"
          },
          {
            name: "variable_fee_control",
            type: "u32"
          },
          {
            name: "bin_step",
            type: "u16"
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
            name: "last_update_timestamp",
            type: "u64"
          },
          {
            name: "bin_step_u128",
            type: "u128"
          },
          {
            name: "sqrt_price_reference",
            type: "u128"
          },
          {
            name: "volatility_accumulator",
            type: "u128"
          },
          {
            name: "volatility_reference",
            type: "u128"
          }
        ]
      }
    },
    {
      name: "EvtClaimPartnerFee",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool",
            type: "pubkey"
          },
          {
            name: "token_a_amount",
            type: "u64"
          },
          {
            name: "token_b_amount",
            type: "u64"
          }
        ]
      }
    },
    {
      name: "EvtClaimPositionFee",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool",
            type: "pubkey"
          },
          {
            name: "position",
            type: "pubkey"
          },
          {
            name: "owner",
            type: "pubkey"
          },
          {
            name: "fee_a_claimed",
            type: "u64"
          },
          {
            name: "fee_b_claimed",
            type: "u64"
          }
        ]
      }
    },
    {
      name: "EvtClaimProtocolFee",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool",
            type: "pubkey"
          },
          {
            name: "token_a_amount",
            type: "u64"
          },
          {
            name: "token_b_amount",
            type: "u64"
          }
        ]
      }
    },
    {
      name: "EvtClaimReward",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool",
            type: "pubkey"
          },
          {
            name: "position",
            type: "pubkey"
          },
          {
            name: "owner",
            type: "pubkey"
          },
          {
            name: "mint_reward",
            type: "pubkey"
          },
          {
            name: "reward_index",
            type: "u8"
          },
          {
            name: "total_reward",
            type: "u64"
          }
        ]
      }
    },
    {
      name: "EvtCloseConfig",
      docs: [
        "Close config"
      ],
      type: {
        kind: "struct",
        fields: [
          {
            name: "config",
            docs: [
              "Config pubkey"
            ],
            type: "pubkey"
          },
          {
            name: "admin",
            docs: [
              "admin pk"
            ],
            type: "pubkey"
          }
        ]
      }
    },
    {
      name: "EvtClosePosition",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool",
            type: "pubkey"
          },
          {
            name: "owner",
            type: "pubkey"
          },
          {
            name: "position",
            type: "pubkey"
          },
          {
            name: "position_nft_mint",
            type: "pubkey"
          }
        ]
      }
    },
    {
      name: "EvtCreateConfig",
      docs: [
        "Create static config"
      ],
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool_fees",
            type: {
              defined: {
                name: "PoolFeeParameters"
              }
            }
          },
          {
            name: "vault_config_key",
            type: "pubkey"
          },
          {
            name: "pool_creator_authority",
            type: "pubkey"
          },
          {
            name: "activation_type",
            type: "u8"
          },
          {
            name: "sqrt_min_price",
            type: "u128"
          },
          {
            name: "sqrt_max_price",
            type: "u128"
          },
          {
            name: "collect_fee_mode",
            type: "u8"
          },
          {
            name: "index",
            type: "u64"
          },
          {
            name: "config",
            type: "pubkey"
          }
        ]
      }
    },
    {
      name: "EvtCreateDynamicConfig",
      docs: [
        "Create dynamic config"
      ],
      type: {
        kind: "struct",
        fields: [
          {
            name: "config",
            type: "pubkey"
          },
          {
            name: "pool_creator_authority",
            type: "pubkey"
          },
          {
            name: "index",
            type: "u64"
          }
        ]
      }
    },
    {
      name: "EvtCreatePosition",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool",
            type: "pubkey"
          },
          {
            name: "owner",
            type: "pubkey"
          },
          {
            name: "position",
            type: "pubkey"
          },
          {
            name: "position_nft_mint",
            type: "pubkey"
          }
        ]
      }
    },
    {
      name: "EvtCreateTokenBadge",
      docs: [
        "Create token badge"
      ],
      type: {
        kind: "struct",
        fields: [
          {
            name: "token_mint",
            type: "pubkey"
          }
        ]
      }
    },
    {
      name: "EvtFundReward",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool",
            type: "pubkey"
          },
          {
            name: "funder",
            type: "pubkey"
          },
          {
            name: "mint_reward",
            type: "pubkey"
          },
          {
            name: "reward_index",
            type: "u8"
          },
          {
            name: "amount",
            type: "u64"
          },
          {
            name: "transfer_fee_excluded_amount_in",
            type: "u64"
          },
          {
            name: "reward_duration_end",
            type: "u64"
          },
          {
            name: "pre_reward_rate",
            type: "u128"
          },
          {
            name: "post_reward_rate",
            type: "u128"
          }
        ]
      }
    },
    {
      name: "EvtInitializePool",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool",
            type: "pubkey"
          },
          {
            name: "token_a_mint",
            type: "pubkey"
          },
          {
            name: "token_b_mint",
            type: "pubkey"
          },
          {
            name: "creator",
            type: "pubkey"
          },
          {
            name: "payer",
            type: "pubkey"
          },
          {
            name: "alpha_vault",
            type: "pubkey"
          },
          {
            name: "pool_fees",
            type: {
              defined: {
                name: "PoolFeeParameters"
              }
            }
          },
          {
            name: "sqrt_min_price",
            type: "u128"
          },
          {
            name: "sqrt_max_price",
            type: "u128"
          },
          {
            name: "activation_type",
            type: "u8"
          },
          {
            name: "collect_fee_mode",
            type: "u8"
          },
          {
            name: "liquidity",
            type: "u128"
          },
          {
            name: "sqrt_price",
            type: "u128"
          },
          {
            name: "activation_point",
            type: "u64"
          },
          {
            name: "token_a_flag",
            type: "u8"
          },
          {
            name: "token_b_flag",
            type: "u8"
          },
          {
            name: "token_a_amount",
            type: "u64"
          },
          {
            name: "token_b_amount",
            type: "u64"
          },
          {
            name: "total_amount_a",
            type: "u64"
          },
          {
            name: "total_amount_b",
            type: "u64"
          },
          {
            name: "pool_type",
            type: "u8"
          }
        ]
      }
    },
    {
      name: "EvtInitializeReward",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool",
            type: "pubkey"
          },
          {
            name: "reward_mint",
            type: "pubkey"
          },
          {
            name: "funder",
            type: "pubkey"
          },
          {
            name: "creator",
            type: "pubkey"
          },
          {
            name: "reward_index",
            type: "u8"
          },
          {
            name: "reward_duration",
            type: "u64"
          }
        ]
      }
    },
    {
      name: "EvtLiquidityChange",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool",
            type: "pubkey"
          },
          {
            name: "position",
            type: "pubkey"
          },
          {
            name: "owner",
            type: "pubkey"
          },
          {
            name: "token_a_amount",
            type: "u64"
          },
          {
            name: "token_b_amount",
            type: "u64"
          },
          {
            name: "transfer_fee_included_token_a_amount",
            type: "u64"
          },
          {
            name: "transfer_fee_included_token_b_amount",
            type: "u64"
          },
          {
            name: "reserve_a_amount",
            type: "u64"
          },
          {
            name: "reserve_b_amount",
            type: "u64"
          },
          {
            name: "liquidity_delta",
            type: "u128"
          },
          {
            name: "token_a_amount_threshold",
            type: "u64"
          },
          {
            name: "token_b_amount_threshold",
            type: "u64"
          },
          {
            name: "change_type",
            type: "u8"
          }
        ]
      }
    },
    {
      name: "EvtLockPosition",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool",
            type: "pubkey"
          },
          {
            name: "position",
            type: "pubkey"
          },
          {
            name: "owner",
            type: "pubkey"
          },
          {
            name: "vesting",
            type: "pubkey"
          },
          {
            name: "cliff_point",
            type: "u64"
          },
          {
            name: "period_frequency",
            type: "u64"
          },
          {
            name: "cliff_unlock_liquidity",
            type: "u128"
          },
          {
            name: "liquidity_per_period",
            type: "u128"
          },
          {
            name: "number_of_period",
            type: "u16"
          }
        ]
      }
    },
    {
      name: "EvtPermanentLockPosition",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool",
            type: "pubkey"
          },
          {
            name: "position",
            type: "pubkey"
          },
          {
            name: "lock_liquidity_amount",
            type: "u128"
          },
          {
            name: "total_permanent_locked_liquidity",
            type: "u128"
          }
        ]
      }
    },
    {
      name: "EvtSetPoolStatus",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool",
            type: "pubkey"
          },
          {
            name: "status",
            type: "u8"
          }
        ]
      }
    },
    {
      name: "EvtSplitPosition2",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool",
            type: "pubkey"
          },
          {
            name: "first_owner",
            type: "pubkey"
          },
          {
            name: "second_owner",
            type: "pubkey"
          },
          {
            name: "first_position",
            type: "pubkey"
          },
          {
            name: "second_position",
            type: "pubkey"
          },
          {
            name: "current_sqrt_price",
            type: "u128"
          },
          {
            name: "amount_splits",
            type: {
              defined: {
                name: "SplitAmountInfo"
              }
            }
          },
          {
            name: "first_position_info",
            type: {
              defined: {
                name: "SplitPositionInfo"
              }
            }
          },
          {
            name: "second_position_info",
            type: {
              defined: {
                name: "SplitPositionInfo"
              }
            }
          },
          {
            name: "split_position_parameters",
            type: {
              defined: {
                name: "SplitPositionParameters2"
              }
            }
          }
        ]
      }
    },
    {
      name: "EvtSwap2",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool",
            type: "pubkey"
          },
          {
            name: "trade_direction",
            type: "u8"
          },
          {
            name: "collect_fee_mode",
            type: "u8"
          },
          {
            name: "has_referral",
            type: "bool"
          },
          {
            name: "params",
            type: {
              defined: {
                name: "SwapParameters2"
              }
            }
          },
          {
            name: "swap_result",
            type: {
              defined: {
                name: "SwapResult2"
              }
            }
          },
          {
            name: "included_transfer_fee_amount_in",
            type: "u64"
          },
          {
            name: "included_transfer_fee_amount_out",
            type: "u64"
          },
          {
            name: "excluded_transfer_fee_amount_out",
            type: "u64"
          },
          {
            name: "current_timestamp",
            type: "u64"
          },
          {
            name: "reserve_a_amount",
            type: "u64"
          },
          {
            name: "reserve_b_amount",
            type: "u64"
          }
        ]
      }
    },
    {
      name: "EvtUpdatePoolFees",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool",
            type: "pubkey"
          },
          {
            name: "operator",
            type: "pubkey"
          },
          {
            name: "params",
            type: {
              defined: {
                name: "UpdatePoolFeesParameters"
              }
            }
          }
        ]
      }
    },
    {
      name: "EvtUpdateRewardDuration",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool",
            type: "pubkey"
          },
          {
            name: "reward_index",
            type: "u8"
          },
          {
            name: "old_reward_duration",
            type: "u64"
          },
          {
            name: "new_reward_duration",
            type: "u64"
          }
        ]
      }
    },
    {
      name: "EvtUpdateRewardFunder",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool",
            type: "pubkey"
          },
          {
            name: "reward_index",
            type: "u8"
          },
          {
            name: "old_funder",
            type: "pubkey"
          },
          {
            name: "new_funder",
            type: "pubkey"
          }
        ]
      }
    },
    {
      name: "EvtWithdrawIneligibleReward",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool",
            type: "pubkey"
          },
          {
            name: "reward_mint",
            type: "pubkey"
          },
          {
            name: "amount",
            type: "u64"
          }
        ]
      }
    },
    {
      name: "InitializeCustomizablePoolParameters",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool_fees",
            docs: [
              "pool fees"
            ],
            type: {
              defined: {
                name: "PoolFeeParameters"
              }
            }
          },
          {
            name: "sqrt_min_price",
            docs: [
              "sqrt min price"
            ],
            type: "u128"
          },
          {
            name: "sqrt_max_price",
            docs: [
              "sqrt max price"
            ],
            type: "u128"
          },
          {
            name: "has_alpha_vault",
            docs: [
              "has alpha vault"
            ],
            type: "bool"
          },
          {
            name: "liquidity",
            docs: [
              "initialize liquidity"
            ],
            type: "u128"
          },
          {
            name: "sqrt_price",
            docs: [
              "The init price of the pool as a sqrt(token_b/token_a) Q64.64 value. Market cap fee scheduler minimum price will be derived from this value"
            ],
            type: "u128"
          },
          {
            name: "activation_type",
            docs: [
              "activation type"
            ],
            type: "u8"
          },
          {
            name: "collect_fee_mode",
            docs: [
              "collect fee mode"
            ],
            type: "u8"
          },
          {
            name: "activation_point",
            docs: [
              "activation point"
            ],
            type: {
              option: "u64"
            }
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
            name: "liquidity",
            docs: [
              "initialize liquidity"
            ],
            type: "u128"
          },
          {
            name: "sqrt_price",
            docs: [
              "The init price of the pool as a sqrt(token_b/token_a) Q64.64 value"
            ],
            type: "u128"
          },
          {
            name: "activation_point",
            docs: [
              "activation point"
            ],
            type: {
              option: "u64"
            }
          }
        ]
      }
    },
    {
      name: "Operator",
      serialization: "bytemuck",
      repr: {
        kind: "c"
      },
      type: {
        kind: "struct",
        fields: [
          {
            name: "whitelisted_address",
            type: "pubkey"
          },
          {
            name: "permission",
            type: "u128"
          },
          {
            name: "padding",
            type: {
              array: [
                "u64",
                2
              ]
            }
          }
        ]
      }
    },
    {
      name: "PodAlignedFeeMarketCapScheduler",
      serialization: "bytemuck",
      repr: {
        kind: "c"
      },
      type: {
        kind: "struct",
        fields: [
          {
            name: "cliff_fee_numerator",
            type: "u64"
          },
          {
            name: "base_fee_mode",
            type: "u8"
          },
          {
            name: "padding",
            type: {
              array: [
                "u8",
                5
              ]
            }
          },
          {
            name: "number_of_period",
            type: "u16"
          },
          {
            name: "sqrt_price_step_bps",
            type: "u32"
          },
          {
            name: "scheduler_expiration_duration",
            type: "u32"
          },
          {
            name: "reduction_factor",
            type: "u64"
          }
        ]
      }
    },
    {
      name: "PodAlignedFeeRateLimiter",
      serialization: "bytemuck",
      repr: {
        kind: "c"
      },
      type: {
        kind: "struct",
        fields: [
          {
            name: "cliff_fee_numerator",
            type: "u64"
          },
          {
            name: "base_fee_mode",
            type: "u8"
          },
          {
            name: "padding",
            type: {
              array: [
                "u8",
                5
              ]
            }
          },
          {
            name: "fee_increment_bps",
            type: "u16"
          },
          {
            name: "max_limiter_duration",
            type: "u32"
          },
          {
            name: "max_fee_bps",
            type: "u32"
          },
          {
            name: "reference_amount",
            type: "u64"
          }
        ]
      }
    },
    {
      name: "PodAlignedFeeTimeScheduler",
      serialization: "bytemuck",
      repr: {
        kind: "c"
      },
      type: {
        kind: "struct",
        fields: [
          {
            name: "cliff_fee_numerator",
            type: "u64"
          },
          {
            name: "base_fee_mode",
            type: "u8"
          },
          {
            name: "padding",
            type: {
              array: [
                "u8",
                5
              ]
            }
          },
          {
            name: "number_of_period",
            type: "u16"
          },
          {
            name: "period_frequency",
            type: "u64"
          },
          {
            name: "reduction_factor",
            type: "u64"
          }
        ]
      }
    },
    {
      name: "Pool",
      serialization: "bytemuck",
      repr: {
        kind: "c"
      },
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool_fees",
            docs: [
              "Pool fee"
            ],
            type: {
              defined: {
                name: "PoolFeesStruct"
              }
            }
          },
          {
            name: "token_a_mint",
            docs: [
              "token a mint"
            ],
            type: "pubkey"
          },
          {
            name: "token_b_mint",
            docs: [
              "token b mint"
            ],
            type: "pubkey"
          },
          {
            name: "token_a_vault",
            docs: [
              "token a vault"
            ],
            type: "pubkey"
          },
          {
            name: "token_b_vault",
            docs: [
              "token b vault"
            ],
            type: "pubkey"
          },
          {
            name: "whitelisted_vault",
            docs: [
              "Whitelisted vault to be able to buy pool before activation_point"
            ],
            type: "pubkey"
          },
          {
            name: "partner",
            docs: [
              "partner"
            ],
            type: "pubkey"
          },
          {
            name: "liquidity",
            docs: [
              "liquidity share"
            ],
            type: "u128"
          },
          {
            name: "_padding",
            docs: [
              "padding, previous reserve amount, be careful to use that field"
            ],
            type: "u128"
          },
          {
            name: "protocol_a_fee",
            docs: [
              "protocol a fee"
            ],
            type: "u64"
          },
          {
            name: "protocol_b_fee",
            docs: [
              "protocol b fee"
            ],
            type: "u64"
          },
          {
            name: "partner_a_fee",
            docs: [
              "partner a fee"
            ],
            type: "u64"
          },
          {
            name: "partner_b_fee",
            docs: [
              "partner b fee"
            ],
            type: "u64"
          },
          {
            name: "sqrt_min_price",
            docs: [
              "min price"
            ],
            type: "u128"
          },
          {
            name: "sqrt_max_price",
            docs: [
              "max price"
            ],
            type: "u128"
          },
          {
            name: "sqrt_price",
            docs: [
              "current price"
            ],
            type: "u128"
          },
          {
            name: "activation_point",
            docs: [
              "Activation point, can be slot or timestamp"
            ],
            type: "u64"
          },
          {
            name: "activation_type",
            docs: [
              "Activation type, 0 means by slot, 1 means by timestamp"
            ],
            type: "u8"
          },
          {
            name: "pool_status",
            docs: [
              "pool status, 0: enable, 1 disable"
            ],
            type: "u8"
          },
          {
            name: "token_a_flag",
            docs: [
              "token a flag"
            ],
            type: "u8"
          },
          {
            name: "token_b_flag",
            docs: [
              "token b flag"
            ],
            type: "u8"
          },
          {
            name: "collect_fee_mode",
            docs: [
              "0 is collect fee in both token, 1 only collect fee only in token b"
            ],
            type: "u8"
          },
          {
            name: "pool_type",
            docs: [
              "pool type"
            ],
            type: "u8"
          },
          {
            name: "version",
            docs: [
              "pool version, 0: max_fee is still capped at 50%, 1: max_fee is capped at 99%"
            ],
            type: "u8"
          },
          {
            name: "_padding_0",
            docs: [
              "padding"
            ],
            type: "u8"
          },
          {
            name: "fee_a_per_liquidity",
            docs: [
              "cumulative"
            ],
            type: {
              array: [
                "u8",
                32
              ]
            }
          },
          {
            name: "fee_b_per_liquidity",
            docs: [
              "cumulative"
            ],
            type: {
              array: [
                "u8",
                32
              ]
            }
          },
          {
            name: "permanent_lock_liquidity",
            type: "u128"
          },
          {
            name: "metrics",
            docs: [
              "metrics"
            ],
            type: {
              defined: {
                name: "PoolMetrics"
              }
            }
          },
          {
            name: "creator",
            docs: [
              "pool creator"
            ],
            type: "pubkey"
          },
          {
            name: "_padding_1",
            docs: [
              "Padding for further use"
            ],
            type: {
              array: [
                "u64",
                6
              ]
            }
          },
          {
            name: "reward_infos",
            docs: [
              "Farming reward information"
            ],
            type: {
              array: [
                {
                  defined: {
                    name: "RewardInfo"
                  }
                },
                2
              ]
            }
          }
        ]
      }
    },
    {
      name: "PoolFeeParameters",
      docs: [
        "Information regarding fee charges"
      ],
      type: {
        kind: "struct",
        fields: [
          {
            name: "base_fee",
            docs: [
              "Base fee"
            ],
            type: {
              defined: {
                name: "BaseFeeParameters"
              }
            }
          },
          {
            name: "dynamic_fee",
            docs: [
              "dynamic fee"
            ],
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
      name: "PoolFeesConfig",
      serialization: "bytemuck",
      repr: {
        kind: "c"
      },
      type: {
        kind: "struct",
        fields: [
          {
            name: "base_fee",
            type: {
              defined: {
                name: "BaseFeeInfo"
              }
            }
          },
          {
            name: "dynamic_fee",
            type: {
              defined: {
                name: "DynamicFeeConfig"
              }
            }
          },
          {
            name: "protocol_fee_percent",
            type: "u8"
          },
          {
            name: "partner_fee_percent",
            type: "u8"
          },
          {
            name: "referral_fee_percent",
            type: "u8"
          },
          {
            name: "padding_0",
            type: {
              array: [
                "u8",
                5
              ]
            }
          },
          {
            name: "padding_1",
            type: {
              array: [
                "u64",
                5
              ]
            }
          }
        ]
      }
    },
    {
      name: "PoolFeesStruct",
      docs: [
        "Information regarding fee charges",
        "trading_fee = amount * trade_fee_numerator / denominator",
        "protocol_fee = trading_fee * protocol_fee_percentage / 100",
        "referral_fee = protocol_fee * referral_percentage / 100",
        "partner_fee = (protocol_fee - referral_fee) * partner_fee_percentage / denominator"
      ],
      serialization: "bytemuck",
      repr: {
        kind: "c"
      },
      type: {
        kind: "struct",
        fields: [
          {
            name: "base_fee",
            docs: [
              "Trade fees are extra token amounts that are held inside the token",
              "accounts during a trade, making the value of liquidity tokens rise.",
              "Trade fee numerator"
            ],
            type: {
              defined: {
                name: "BaseFeeStruct"
              }
            }
          },
          {
            name: "protocol_fee_percent",
            docs: [
              "Protocol trading fees are extra token amounts that are held inside the token",
              "accounts during a trade, with the equivalent in pool tokens minted to",
              "the protocol of the program.",
              "Protocol trade fee numerator"
            ],
            type: "u8"
          },
          {
            name: "partner_fee_percent",
            docs: [
              "partner fee"
            ],
            type: "u8"
          },
          {
            name: "referral_fee_percent",
            docs: [
              "referral fee"
            ],
            type: "u8"
          },
          {
            name: "padding_0",
            docs: [
              "padding"
            ],
            type: {
              array: [
                "u8",
                5
              ]
            }
          },
          {
            name: "dynamic_fee",
            docs: [
              "dynamic fee"
            ],
            type: {
              defined: {
                name: "DynamicFeeStruct"
              }
            }
          },
          {
            name: "init_sqrt_price",
            type: "u128"
          }
        ]
      }
    },
    {
      name: "PoolMetrics",
      serialization: "bytemuck",
      repr: {
        kind: "c"
      },
      type: {
        kind: "struct",
        fields: [
          {
            name: "total_lp_a_fee",
            type: "u128"
          },
          {
            name: "total_lp_b_fee",
            type: "u128"
          },
          {
            name: "total_protocol_a_fee",
            type: "u64"
          },
          {
            name: "total_protocol_b_fee",
            type: "u64"
          },
          {
            name: "total_partner_a_fee",
            type: "u64"
          },
          {
            name: "total_partner_b_fee",
            type: "u64"
          },
          {
            name: "total_position",
            type: "u64"
          },
          {
            name: "padding",
            type: "u64"
          }
        ]
      }
    },
    {
      name: "Position",
      serialization: "bytemuck",
      repr: {
        kind: "c"
      },
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool",
            type: "pubkey"
          },
          {
            name: "nft_mint",
            docs: [
              "nft mint"
            ],
            type: "pubkey"
          },
          {
            name: "fee_a_per_token_checkpoint",
            docs: [
              "fee a checkpoint"
            ],
            type: {
              array: [
                "u8",
                32
              ]
            }
          },
          {
            name: "fee_b_per_token_checkpoint",
            docs: [
              "fee b checkpoint"
            ],
            type: {
              array: [
                "u8",
                32
              ]
            }
          },
          {
            name: "fee_a_pending",
            docs: [
              "fee a pending"
            ],
            type: "u64"
          },
          {
            name: "fee_b_pending",
            docs: [
              "fee b pending"
            ],
            type: "u64"
          },
          {
            name: "unlocked_liquidity",
            docs: [
              "unlock liquidity"
            ],
            type: "u128"
          },
          {
            name: "vested_liquidity",
            docs: [
              "vesting liquidity"
            ],
            type: "u128"
          },
          {
            name: "permanent_locked_liquidity",
            docs: [
              "permanent locked liquidity"
            ],
            type: "u128"
          },
          {
            name: "metrics",
            docs: [
              "metrics"
            ],
            type: {
              defined: {
                name: "PositionMetrics"
              }
            }
          },
          {
            name: "reward_infos",
            docs: [
              "Farming reward information"
            ],
            type: {
              array: [
                {
                  defined: {
                    name: "UserRewardInfo"
                  }
                },
                2
              ]
            }
          },
          {
            name: "padding",
            docs: [
              "padding for future usage"
            ],
            type: {
              array: [
                "u128",
                6
              ]
            }
          }
        ]
      }
    },
    {
      name: "PositionMetrics",
      serialization: "bytemuck",
      repr: {
        kind: "c"
      },
      type: {
        kind: "struct",
        fields: [
          {
            name: "total_claimed_a_fee",
            type: "u64"
          },
          {
            name: "total_claimed_b_fee",
            type: "u64"
          }
        ]
      }
    },
    {
      name: "RemoveLiquidityParameters",
      type: {
        kind: "struct",
        fields: [
          {
            name: "liquidity_delta",
            docs: [
              "delta liquidity"
            ],
            type: "u128"
          },
          {
            name: "token_a_amount_threshold",
            docs: [
              "minimum token a amount"
            ],
            type: "u64"
          },
          {
            name: "token_b_amount_threshold",
            docs: [
              "minimum token b amount"
            ],
            type: "u64"
          }
        ]
      }
    },
    {
      name: "RewardInfo",
      docs: [
        "Stores the state relevant for tracking liquidity mining rewards"
      ],
      serialization: "bytemuck",
      repr: {
        kind: "c"
      },
      type: {
        kind: "struct",
        fields: [
          {
            name: "initialized",
            docs: [
              "Indicates if the reward has been initialized"
            ],
            type: "u8"
          },
          {
            name: "reward_token_flag",
            docs: [
              "reward token flag"
            ],
            type: "u8"
          },
          {
            name: "_padding_0",
            docs: [
              "padding"
            ],
            type: {
              array: [
                "u8",
                6
              ]
            }
          },
          {
            name: "_padding_1",
            docs: [
              "Padding to ensure `reward_rate: u128` is 16-byte aligned"
            ],
            type: {
              array: [
                "u8",
                8
              ]
            }
          },
          {
            name: "mint",
            docs: [
              "Reward token mint."
            ],
            type: "pubkey"
          },
          {
            name: "vault",
            docs: [
              "Reward vault token account."
            ],
            type: "pubkey"
          },
          {
            name: "funder",
            docs: [
              "Authority account that allows to fund rewards"
            ],
            type: "pubkey"
          },
          {
            name: "reward_duration",
            docs: [
              "reward duration"
            ],
            type: "u64"
          },
          {
            name: "reward_duration_end",
            docs: [
              "reward duration end"
            ],
            type: "u64"
          },
          {
            name: "reward_rate",
            docs: [
              "reward rate"
            ],
            type: "u128"
          },
          {
            name: "reward_per_token_stored",
            docs: [
              "Reward per token stored"
            ],
            type: {
              array: [
                "u8",
                32
              ]
            }
          },
          {
            name: "last_update_time",
            docs: [
              "The last time reward states were updated."
            ],
            type: "u64"
          },
          {
            name: "cumulative_seconds_with_empty_liquidity_reward",
            docs: [
              "Accumulated seconds when the farm distributed rewards but the bin was empty.",
              "These rewards will be carried over to the next reward time window."
            ],
            type: "u64"
          }
        ]
      }
    },
    {
      name: "SplitAmountInfo",
      type: {
        kind: "struct",
        fields: [
          {
            name: "permanent_locked_liquidity",
            type: "u128"
          },
          {
            name: "unlocked_liquidity",
            type: "u128"
          },
          {
            name: "fee_a",
            type: "u64"
          },
          {
            name: "fee_b",
            type: "u64"
          },
          {
            name: "reward_0",
            type: "u64"
          },
          {
            name: "reward_1",
            type: "u64"
          }
        ]
      }
    },
    {
      name: "SplitPositionInfo",
      type: {
        kind: "struct",
        fields: [
          {
            name: "liquidity",
            type: "u128"
          },
          {
            name: "fee_a",
            type: "u64"
          },
          {
            name: "fee_b",
            type: "u64"
          },
          {
            name: "reward_0",
            type: "u64"
          },
          {
            name: "reward_1",
            type: "u64"
          }
        ]
      }
    },
    {
      name: "SplitPositionParameters",
      type: {
        kind: "struct",
        fields: [
          {
            name: "unlocked_liquidity_percentage",
            docs: [
              "Percentage of unlocked liquidity to split to the second position"
            ],
            type: "u8"
          },
          {
            name: "permanent_locked_liquidity_percentage",
            docs: [
              "Percentage of permanent locked liquidity to split to the second position"
            ],
            type: "u8"
          },
          {
            name: "fee_a_percentage",
            docs: [
              "Percentage of fee A pending to split to the second position"
            ],
            type: "u8"
          },
          {
            name: "fee_b_percentage",
            docs: [
              "Percentage of fee B pending to split to the second position"
            ],
            type: "u8"
          },
          {
            name: "reward_0_percentage",
            docs: [
              "Percentage of reward 0 pending to split to the second position"
            ],
            type: "u8"
          },
          {
            name: "reward_1_percentage",
            docs: [
              "Percentage of reward 1 pending to split to the second position"
            ],
            type: "u8"
          },
          {
            name: "padding",
            docs: [
              "padding for future"
            ],
            type: {
              array: [
                "u8",
                16
              ]
            }
          }
        ]
      }
    },
    {
      name: "SplitPositionParameters2",
      type: {
        kind: "struct",
        fields: [
          {
            name: "unlocked_liquidity_numerator",
            type: "u32"
          },
          {
            name: "permanent_locked_liquidity_numerator",
            type: "u32"
          },
          {
            name: "fee_a_numerator",
            type: "u32"
          },
          {
            name: "fee_b_numerator",
            type: "u32"
          },
          {
            name: "reward_0_numerator",
            type: "u32"
          },
          {
            name: "reward_1_numerator",
            type: "u32"
          }
        ]
      }
    },
    {
      name: "StaticConfigParameters",
      type: {
        kind: "struct",
        fields: [
          {
            name: "pool_fees",
            type: {
              defined: {
                name: "PoolFeeParameters"
              }
            }
          },
          {
            name: "sqrt_min_price",
            type: "u128"
          },
          {
            name: "sqrt_max_price",
            type: "u128"
          },
          {
            name: "vault_config_key",
            type: "pubkey"
          },
          {
            name: "pool_creator_authority",
            type: "pubkey"
          },
          {
            name: "activation_type",
            type: "u8"
          },
          {
            name: "collect_fee_mode",
            type: "u8"
          }
        ]
      }
    },
    {
      name: "SwapParameters",
      type: {
        kind: "struct",
        fields: [
          {
            name: "amount_in",
            type: "u64"
          },
          {
            name: "minimum_amount_out",
            type: "u64"
          }
        ]
      }
    },
    {
      name: "SwapParameters2",
      type: {
        kind: "struct",
        fields: [
          {
            name: "amount_0",
            docs: [
              "When it's exact in, partial fill, this will be amount_in. When it's exact out, this will be amount_out"
            ],
            type: "u64"
          },
          {
            name: "amount_1",
            docs: [
              "When it's exact in, partial fill, this will be minimum_amount_out. When it's exact out, this will be maximum_amount_in"
            ],
            type: "u64"
          },
          {
            name: "swap_mode",
            docs: [
              "Swap mode, refer [SwapMode]"
            ],
            type: "u8"
          }
        ]
      }
    },
    {
      name: "SwapResult2",
      type: {
        kind: "struct",
        fields: [
          {
            name: "included_fee_input_amount",
            type: "u64"
          },
          {
            name: "excluded_fee_input_amount",
            type: "u64"
          },
          {
            name: "amount_left",
            type: "u64"
          },
          {
            name: "output_amount",
            type: "u64"
          },
          {
            name: "next_sqrt_price",
            type: "u128"
          },
          {
            name: "trading_fee",
            type: "u64"
          },
          {
            name: "protocol_fee",
            type: "u64"
          },
          {
            name: "partner_fee",
            type: "u64"
          },
          {
            name: "referral_fee",
            type: "u64"
          }
        ]
      }
    },
    {
      name: "TokenBadge",
      docs: [
        "Parameter that set by the protocol"
      ],
      serialization: "bytemuck",
      repr: {
        kind: "c"
      },
      type: {
        kind: "struct",
        fields: [
          {
            name: "token_mint",
            docs: [
              "token mint"
            ],
            type: "pubkey"
          },
          {
            name: "_padding",
            docs: [
              "Reserve"
            ],
            type: {
              array: [
                "u8",
                128
              ]
            }
          }
        ]
      }
    },
    {
      name: "UpdatePoolFeesParameters",
      type: {
        kind: "struct",
        fields: [
          {
            name: "cliff_fee_numerator",
            docs: [
              "Base fee update mode:",
              "- None: skip base fee update",
              "- Some: update new cliff_fee_numerator if base fee is static"
            ],
            type: {
              option: "u64"
            }
          },
          {
            name: "dynamic_fee",
            docs: [
              "Dynamic fee update mode:",
              "- None: skip dynamic fee update",
              "- Some(with default value): disable dynamic fee",
              "- Some(with non default value): enable dynamic fee if disabled or update dynamic fee if enabled"
            ],
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
      name: "UserRewardInfo",
      serialization: "bytemuck",
      repr: {
        kind: "c"
      },
      type: {
        kind: "struct",
        fields: [
          {
            name: "reward_per_token_checkpoint",
            docs: [
              "The latest update reward checkpoint"
            ],
            type: {
              array: [
                "u8",
                32
              ]
            }
          },
          {
            name: "reward_pendings",
            docs: [
              "Current pending rewards"
            ],
            type: "u64"
          },
          {
            name: "total_claimed_rewards",
            docs: [
              "Total claimed rewards"
            ],
            type: "u64"
          }
        ]
      }
    },
    {
      name: "Vesting",
      serialization: "bytemuck",
      repr: {
        kind: "c"
      },
      type: {
        kind: "struct",
        fields: [
          {
            name: "position",
            type: "pubkey"
          },
          {
            name: "cliff_point",
            type: "u64"
          },
          {
            name: "period_frequency",
            type: "u64"
          },
          {
            name: "cliff_unlock_liquidity",
            type: "u128"
          },
          {
            name: "liquidity_per_period",
            type: "u128"
          },
          {
            name: "total_released_liquidity",
            type: "u128"
          },
          {
            name: "number_of_period",
            type: "u16"
          },
          {
            name: "padding",
            type: {
              array: [
                "u8",
                14
              ]
            }
          },
          {
            name: "padding2",
            type: {
              array: [
                "u128",
                4
              ]
            }
          }
        ]
      }
    },
    {
      name: "VestingParameters",
      type: {
        kind: "struct",
        fields: [
          {
            name: "cliff_point",
            type: {
              option: "u64"
            }
          },
          {
            name: "period_frequency",
            type: "u64"
          },
          {
            name: "cliff_unlock_liquidity",
            type: "u128"
          },
          {
            name: "liquidity_per_period",
            type: "u128"
          },
          {
            name: "number_of_period",
            type: "u16"
          }
        ]
      }
    }
  ],
  constants: [
    {
      name: "BIN_STEP_BPS_DEFAULT",
      type: "u16",
      value: "1"
    },
    {
      name: "BIN_STEP_U128_DEFAULT_LE_BYTES",
      type: {
        array: [
          "u8",
          16
        ]
      },
      value: "[203, 16, 199, 186, 184, 141, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0]"
    },
    {
      name: "CUSTOMIZABLE_POOL_PREFIX",
      type: "bytes",
      value: "[99, 112, 111, 111, 108]"
    },
    {
      name: "FEE_DENOMINATOR",
      docs: [
        "Default fee denominator. DO NOT simply update it as it will break logic that depends on it as default value."
      ],
      type: "u64",
      value: "1000000000"
    },
    {
      name: "MAX_BASIS_POINT",
      docs: [
        "Max basis point. 100% in pct"
      ],
      type: "u64",
      value: "10000"
    },
    {
      name: "MAX_SQRT_PRICE_LE_BYTES",
      type: {
        array: [
          "u8",
          16
        ]
      },
      value: "[155, 87, 105, 78, 169, 26, 92, 132, 177, 196, 254, 255, 0, 0, 0, 0]"
    },
    {
      name: "MIN_SQRT_PRICE_LE_BYTES",
      type: {
        array: [
          "u8",
          16
        ]
      },
      value: "[80, 59, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]"
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
      name: "POSITION_NFT_ACCOUNT_PREFIX",
      type: "bytes",
      value: "[112, 111, 115, 105, 116, 105, 111, 110, 95, 110, 102, 116, 95, 97, 99, 99, 111, 117, 110, 116]"
    },
    {
      name: "POSITION_PREFIX",
      type: "bytes",
      value: "[112, 111, 115, 105, 116, 105, 111, 110]"
    },
    {
      name: "SPLIT_POSITION_DENOMINATOR",
      type: "u32",
      value: "1000000000"
    },
    {
      name: "TOKEN_VAULT_PREFIX",
      type: "bytes",
      value: "[116, 111, 107, 101, 110, 95, 118, 97, 117, 108, 116]"
    }
  ]
};

// src/helpers/createProgram.ts
function createClawlabProgram(connection) {
  const provider = new anchor.AnchorProvider(connection, null, {
    commitment: connection.commitment
  });
  const program = new anchor.Program(
    idl_default,
    provider
  );
  return { program };
}
function createDammV2Program(connection) {
  const provider = new anchor.AnchorProvider(connection, null, {
    commitment: connection.commitment
  });
  const program = new anchor.Program(idl_default2, provider);
  return program;
}
var getOrCreateATAInstruction = async (connection, tokenMint, owner, payer, allowOwnerOffCurve = true, tokenProgram) => {
  const toAccount = splToken.getAssociatedTokenAddressSync(
    tokenMint,
    owner,
    allowOwnerOffCurve,
    tokenProgram
  );
  try {
    await splToken.getAccount(connection, toAccount);
    return { ataPubkey: toAccount, ix: void 0 };
  } catch (e) {
    if (e instanceof splToken.TokenAccountNotFoundError || e instanceof splToken.TokenInvalidAccountOwnerError) {
      const ix = splToken.createAssociatedTokenAccountIdempotentInstruction(
        payer,
        toAccount,
        owner,
        tokenMint,
        tokenProgram
      );
      return { ataPubkey: toAccount, ix };
    } else {
      console.error("Error::getOrCreateATAInstruction", e);
      throw e;
    }
  }
};
function unwrapSOLInstruction(owner, receiver, allowOwnerOffCurve = true) {
  const wSolATAAccount = splToken.getAssociatedTokenAddressSync(
    splToken.NATIVE_MINT,
    owner,
    allowOwnerOffCurve
  );
  if (wSolATAAccount) {
    const closedWrappedSolInstruction = splToken.createCloseAccountInstruction(
      wSolATAAccount,
      receiver,
      owner,
      [],
      splToken.TOKEN_PROGRAM_ID
    );
    return closedWrappedSolInstruction;
  }
  return null;
}
function wrapSOLInstruction(from, to, amount) {
  return [
    web3_js.SystemProgram.transfer({
      fromPubkey: from,
      toPubkey: to,
      lamports: amount
    }),
    splToken.createSyncNativeInstruction(
      to,
      splToken.TOKEN_PROGRAM_ID
    )
  ];
}
function findAssociatedTokenAddress(walletAddress, tokenMintAddress, tokenProgramId) {
  return web3_js.PublicKey.findProgramAddressSync(
    [
      walletAddress.toBuffer(),
      tokenProgramId.toBuffer(),
      tokenMintAddress.toBuffer()
    ],
    splToken.ASSOCIATED_TOKEN_PROGRAM_ID
  )[0];
}
var SEED = Object.freeze({
  POOL_AUTHORITY: "pool_authority",
  EVENT_AUTHORITY: "__event_authority",
  CONFIG: "config",
  POOL: "pool",
  BASE_VAULT: "base_vault",
  QUOTE_VAULT: "quote_vault",
  USER_TOKEN_ACCOUNT: "user_token_account",
  METADATA: "metadata"
});
function deriveConfig() {
  const [config] = web3_js.PublicKey.findProgramAddressSync(
    [Buffer.from(SEED.CONFIG)],
    CLAWLAB_PROGRAM_ID
  );
  return config;
}
function derivePoolAuthority() {
  const [poolAuthority] = web3_js.PublicKey.findProgramAddressSync(
    [Buffer.from(SEED.POOL_AUTHORITY)],
    CLAWLAB_PROGRAM_ID
  );
  return poolAuthority;
}
function deriveEventAuthority() {
  const [eventAuthority] = web3_js.PublicKey.findProgramAddressSync(
    [Buffer.from(SEED.EVENT_AUTHORITY)],
    CLAWLAB_PROGRAM_ID
  );
  return eventAuthority;
}
function derivePool(baseMint, quoteMint) {
  const [pool] = web3_js.PublicKey.findProgramAddressSync(
    [Buffer.from(SEED.POOL), baseMint.toBuffer(), quoteMint.toBuffer()],
    CLAWLAB_PROGRAM_ID
  );
  return pool;
}
function deriveBaseVault(baseMint, config) {
  const [vault] = web3_js.PublicKey.findProgramAddressSync(
    [Buffer.from(SEED.BASE_VAULT), config.toBuffer(), baseMint.toBuffer()],
    CLAWLAB_PROGRAM_ID
  );
  return vault;
}
function deriveQuoteVault(quoteMint, config) {
  const [vault] = web3_js.PublicKey.findProgramAddressSync(
    [Buffer.from(SEED.QUOTE_VAULT), config.toBuffer(), quoteMint.toBuffer()],
    CLAWLAB_PROGRAM_ID
  );
  return vault;
}
function deriveUserTokenAccount(baseMint, user) {
  const [userOutputTokenAccount] = web3_js.PublicKey.findProgramAddressSync(
    [Buffer.from(SEED.USER_TOKEN_ACCOUNT), baseMint.toBuffer(), user.toBuffer()],
    CLAWLAB_PROGRAM_ID
  );
  return userOutputTokenAccount;
}
function deriveMintMetadata(baseMint) {
  const [mintMetadata] = web3_js.PublicKey.findProgramAddressSync(
    [Buffer.from(SEED.METADATA), METAPLEX_PROGRAM_ID.toBuffer(), baseMint.toBuffer()],
    METAPLEX_PROGRAM_ID
  );
  return mintMetadata;
}

// src/services/program.ts
var ClawlabProgram = class {
  constructor(connection) {
    const { program } = createClawlabProgram(connection);
    this.program = program;
    this.connection = connection;
    this.poolAuthority = derivePoolAuthority();
    this.eventAuthority = deriveEventAuthority();
    this.config = deriveConfig();
  }
  async prepareTokenAccounts(owner, payer, tokenAMint, tokenBMint, tokenAProgram, tokenBProgram) {
    const instructions = [];
    const [
      { ataPubkey: ataTokenA, ix: createAtaTokenAIx },
      { ataPubkey: ataTokenB, ix: createAtaTokenBIx }
    ] = await Promise.all([
      getOrCreateATAInstruction(
        this.connection,
        tokenAMint,
        owner,
        payer,
        true,
        tokenAProgram
      ),
      getOrCreateATAInstruction(
        this.connection,
        tokenBMint,
        owner,
        payer,
        true,
        tokenBProgram
      )
    ]);
    createAtaTokenAIx && instructions.push(createAtaTokenAIx);
    createAtaTokenBIx && instructions.push(createAtaTokenBIx);
    return { ataTokenA, ataTokenB, instructions };
  }
  /**
   * Get the underlying program instance
   * @returns The program instance
   */
  getProgram() {
    return this.program;
  }
};

// src/services/state.ts
var StateService = class extends ClawlabProgram {
  constructor(connection) {
    super(connection);
  }
  async getConfig() {
    return getAccountData(
      this.config,
      "config",
      this.program,
      this.connection.commitment
    );
  }
  async getPoolConfig(poolAddress) {
    return getAccountData(
      poolAddress,
      "poolConfig",
      this.program,
      this.connection.commitment
    );
  }
};

// src/services/creator.ts
var CreatorService = class extends ClawlabProgram {
  constructor(connection) {
    super(connection);
    this.state = new StateService(connection);
  }
  async claimCreatorFeeIx(payer, baseMint, quoteMint, outputTokenAccount) {
    const poolAddress = derivePool(baseMint, quoteMint);
    const quoteVault = deriveQuoteVault(quoteMint, this.config);
    return this.program.methods.claimCreator().accountsPartial({
      poolAuthority: this.poolAuthority,
      config: this.config,
      baseMint,
      quoteMint,
      pool: poolAddress,
      quoteVault,
      tokenAccount: outputTokenAccount,
      tokenBaseProgram: splToken.TOKEN_PROGRAM_ID,
      tokenQuoteProgram: splToken.TOKEN_PROGRAM_ID,
      payer,
      eventAuthority: this.eventAuthority,
      program: CLAWLAB_PROGRAM_ID
    }).instruction();
  }
  async ClaimFeeIx(payer, baseMint, quoteMint, outputTokenAccount) {
    return this.claimCreatorFeeIx(payer, baseMint, quoteMint, outputTokenAccount);
  }
  async ClaimFeeTx(params) {
    const {
      payer,
      baseMint
    } = params;
    const quoteMint = splToken.NATIVE_MINT;
    const preInstructions = [];
    const postInstructions = [];
    const { ataPubkey: quoteMintAta, ix: createQuoteMintAtaIx } = await getOrCreateATAInstruction(
      this.connection,
      quoteMint,
      payer,
      payer,
      true,
      splToken.TOKEN_PROGRAM_ID
    );
    createQuoteMintAtaIx && preInstructions.push(createQuoteMintAtaIx);
    const createPoolIx = await this.claimCreatorFeeIx(payer, baseMint, quoteMint, quoteMintAta);
    const unwrapSolIx = unwrapSOLInstruction(payer, payer);
    unwrapSolIx && postInstructions.push(unwrapSolIx);
    return new web3_js.Transaction().add(...preInstructions, createPoolIx, ...postInstructions);
  }
};
var PoolService = class extends ClawlabProgram {
  constructor(connection) {
    super(connection);
    this.state = new StateService(connection);
  }
  async initializePoolIx(payer, baseMint, quoteMint, params) {
    const poolAddress = derivePool(baseMint, quoteMint);
    const baseVault = deriveBaseVault(baseMint, this.config);
    const quoteVault = deriveQuoteVault(quoteMint, this.config);
    const mintMetadata = deriveMintMetadata(baseMint);
    return this.program.methods.initializeSplPool(params).accountsPartial({
      poolAuthority: this.poolAuthority,
      config: this.config,
      baseMint,
      quoteMint,
      pool: poolAddress,
      baseVault,
      quoteVault,
      mintMetadata,
      metadataProgram: METAPLEX_PROGRAM_ID,
      tokenBaseProgram: splToken.TOKEN_PROGRAM_ID,
      tokenQuoteProgram: splToken.TOKEN_PROGRAM_ID,
      payer,
      systemProgram: web3_js.SystemProgram.programId,
      eventAuthority: this.eventAuthority,
      program: CLAWLAB_PROGRAM_ID
    }).instruction();
  }
  async CreateIx(payer, baseMint, quoteMint, params) {
    return this.initializePoolIx(
      payer,
      baseMint,
      quoteMint,
      params
    );
  }
  async CreateTx(params) {
    const {
      payer,
      baseMint,
      ...initializeParam
    } = params;
    const quoteMint = splToken.NATIVE_MINT;
    const createPoolIx = await this.initializePoolIx(payer, baseMint, quoteMint, initializeParam);
    return new web3_js.Transaction().add(createPoolIx);
  }
  async buyTokenIx(payer, baseMint, quoteMint, inputTokenAccount, outputTokenAccount, userTokenAccount, params) {
    const poolAddress = derivePool(baseMint, quoteMint);
    const baseVault = deriveBaseVault(baseMint, this.config);
    const quoteVault = deriveQuoteVault(quoteMint, this.config);
    return this.program.methods.buyToken(params).accountsPartial({
      poolAuthority: this.poolAuthority,
      config: this.config,
      baseMint,
      quoteMint,
      pool: poolAddress,
      baseVault,
      quoteVault,
      inputTokenAccount,
      outputTokenAccount,
      userTokenAccount,
      payer,
      tokenBaseProgram: splToken.TOKEN_PROGRAM_ID,
      tokenQuoteProgram: splToken.TOKEN_PROGRAM_ID,
      systemProgram: web3_js.SystemProgram.programId,
      eventAuthority: this.eventAuthority,
      program: CLAWLAB_PROGRAM_ID
    }).instruction();
  }
  async MintToIx(payer, baseMint, quoteMint, inputTokenAccount, outputTokenAccount, userTokenAccount, params) {
    return this.buyTokenIx(
      payer,
      baseMint,
      quoteMint,
      inputTokenAccount,
      outputTokenAccount,
      userTokenAccount,
      params
    );
  }
  async MintToTx(params) {
    const {
      payer,
      baseMint,
      ...mintToParam
    } = params;
    const quoteMint = splToken.NATIVE_MINT;
    const preInstructions = [];
    const postInstructions = [];
    const userTokenAccount = deriveUserTokenAccount(baseMint, payer);
    const { ataPubkey: quoteMintAta, ix: createQuoteMintAtaIx } = await getOrCreateATAInstruction(
      this.connection,
      quoteMint,
      payer,
      payer,
      true,
      splToken.TOKEN_PROGRAM_ID
    );
    createQuoteMintAtaIx && preInstructions.push(createQuoteMintAtaIx);
    const amountIn = params.copies.mul(new BN__default.default(2e8));
    preInstructions.push(...wrapSOLInstruction(payer, quoteMintAta, BigInt(amountIn.toString())));
    const { ataPubkey: baseMintAta, ix: createBaseMintAtaIx } = await getOrCreateATAInstruction(
      this.connection,
      baseMint,
      payer,
      payer,
      true,
      splToken.TOKEN_PROGRAM_ID
    );
    createBaseMintAtaIx && preInstructions.push(createBaseMintAtaIx);
    const mintToIx = await this.buyTokenIx(
      payer,
      baseMint,
      quoteMint,
      quoteMintAta,
      baseMintAta,
      userTokenAccount,
      mintToParam
    );
    const unwrapSolIx = unwrapSOLInstruction(payer, payer);
    unwrapSolIx && postInstructions.push(unwrapSolIx);
    return new web3_js.Transaction().add(...preInstructions, mintToIx, ...postInstructions);
  }
  async refundTokenIx(payer, baseMint, quoteMint, userTokenAccount, outputTokenAccount) {
    const poolAddress = derivePool(baseMint, quoteMint);
    const baseVault = deriveBaseVault(baseMint, this.config);
    const quoteVault = deriveQuoteVault(quoteMint, this.config);
    return this.program.methods.refundToken().accountsPartial({
      poolAuthority: this.poolAuthority,
      config: this.config,
      baseMint,
      quoteMint,
      pool: poolAddress,
      baseVault,
      quoteVault,
      inputTokenAccount: userTokenAccount,
      outputTokenAccount,
      tokenBaseProgram: splToken.TOKEN_PROGRAM_ID,
      tokenQuoteProgram: splToken.TOKEN_PROGRAM_ID,
      payer,
      systemProgram: web3_js.SystemProgram.programId,
      eventAuthority: this.eventAuthority,
      program: CLAWLAB_PROGRAM_ID
    }).instruction();
  }
  async RefundIx(payer, baseMint, quoteMint, userTokenAccount, outputTokenAccount) {
    return this.refundTokenIx(
      payer,
      baseMint,
      quoteMint,
      userTokenAccount,
      outputTokenAccount
    );
  }
  async RefundTx(params) {
    const {
      payer,
      baseMint
    } = params;
    const quoteMint = splToken.NATIVE_MINT;
    const preInstructions = [];
    const postInstructions = [];
    const userTokenAccount = deriveUserTokenAccount(baseMint, payer);
    const { ataPubkey: quoteMintAta, ix: createQuoteMintAtaIx } = await getOrCreateATAInstruction(
      this.connection,
      quoteMint,
      payer,
      payer,
      true,
      splToken.TOKEN_PROGRAM_ID
    );
    createQuoteMintAtaIx && preInstructions.push(createQuoteMintAtaIx);
    const refundIx = await this.refundTokenIx(
      payer,
      baseMint,
      quoteMint,
      userTokenAccount,
      quoteMintAta
    );
    const unwrapSolIx = unwrapSOLInstruction(payer, payer);
    unwrapSolIx && postInstructions.push(unwrapSolIx);
    return new web3_js.Transaction().add(...preInstructions, refundIx, ...postInstructions);
  }
};
var UserService = class extends ClawlabProgram {
  constructor(connection) {
    super(connection);
    this.state = new StateService(connection);
  }
  async claimUserTokenIx(payer, baseMint, quoteMint, inputTokenAccount, outputTokenAccount) {
    const poolAddress = derivePool(baseMint, quoteMint);
    return this.program.methods.claimUserToken().accountsPartial({
      poolAuthority: this.poolAuthority,
      baseMint,
      quoteMint,
      pool: poolAddress,
      inputTokenAccount,
      outputTokenAccount,
      tokenBaseProgram: splToken.TOKEN_PROGRAM_ID,
      tokenQuoteProgram: splToken.TOKEN_PROGRAM_ID,
      payer,
      eventAuthority: this.eventAuthority,
      program: CLAWLAB_PROGRAM_ID
    }).instruction();
  }
  async ClaimTokenIx(payer, baseMint, quoteMint, inputTokenAccount, outputTokenAccount) {
    return this.claimUserTokenIx(payer, baseMint, quoteMint, inputTokenAccount, outputTokenAccount);
  }
  async ClaimTokenTx(params) {
    const {
      payer,
      baseMint
    } = params;
    const quoteMint = splToken.NATIVE_MINT;
    const userTokenAccount = deriveUserTokenAccount(baseMint, payer);
    const preInstructions = [];
    const { ataPubkey: baseMintAta, ix: createBaseMintAtaIx } = await getOrCreateATAInstruction(
      this.connection,
      baseMint,
      payer,
      payer,
      true,
      splToken.TOKEN_PROGRAM_ID
    );
    createBaseMintAtaIx && preInstructions.push(createBaseMintAtaIx);
    const claimUserTokenIx = await this.claimUserTokenIx(payer, baseMint, quoteMint, userTokenAccount, baseMintAta);
    return new web3_js.Transaction().add(...preInstructions, claimUserTokenIx);
  }
};

// src/client.ts
var ClawlabClient = class _ClawlabClient {
  constructor(connection) {
    this.state = new StateService(connection);
    this.user = new UserService(connection);
    this.creator = new CreatorService(connection);
    this.pool = new PoolService(connection);
    this.connection = connection;
  }
  static create(connection, commitment = "confirmed") {
    return new _ClawlabClient(connection);
  }
};

exports.CLAWLAB_PROGRAM_ID = CLAWLAB_PROGRAM_ID;
exports.ClawlabClient = ClawlabClient;
exports.ClawlabIdl = idl_default;
exports.ClawlabProgram = ClawlabProgram;
exports.CreatorService = CreatorService;
exports.DAMM_V2_PROGRAM_ID = DAMM_V2_PROGRAM_ID;
exports.METAPLEX_PROGRAM_ID = METAPLEX_PROGRAM_ID;
exports.PoolService = PoolService;
exports.StateService = StateService;
exports.UserService = UserService;
exports.createClawlabProgram = createClawlabProgram;
exports.createDammV2Program = createDammV2Program;
exports.deriveBaseVault = deriveBaseVault;
exports.deriveConfig = deriveConfig;
exports.deriveEventAuthority = deriveEventAuthority;
exports.deriveMintMetadata = deriveMintMetadata;
exports.derivePool = derivePool;
exports.derivePoolAuthority = derivePoolAuthority;
exports.deriveQuoteVault = deriveQuoteVault;
exports.deriveUserTokenAccount = deriveUserTokenAccount;
exports.findAssociatedTokenAddress = findAssociatedTokenAddress;
exports.getAccountCreationTimestamp = getAccountCreationTimestamp;
exports.getAccountCreationTimestamps = getAccountCreationTimestamps;
exports.getAccountData = getAccountData;
exports.getOrCreateATAInstruction = getOrCreateATAInstruction;
exports.getTotalTokenSupply = getTotalTokenSupply;
exports.unwrapSOLInstruction = unwrapSOLInstruction;
exports.wrapSOLInstruction = wrapSOLInstruction;
//# sourceMappingURL=index.js.map
//# sourceMappingURL=index.js.map