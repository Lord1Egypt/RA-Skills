import Workflow from "/assets/v3/components/workflow.js"
import AlertDialog from "/assets/v3/components/alert_dialog.js";
import ConfirmDialog from "/assets/v3/components/confirm_dialog.js"
import {_WF_} from "/assets/v3/components/workflow.js"
import Language from "./language.js"
import {decodeExt} from '/assets/v3/settings/config.js';

//workflow会在其他服务中打开，不可以注入tags、service，所以单独加载，组件也需要单独加载
const sole_tags = Platform.language().indexOf("zh") == 0 ? Language.zh : Language.en;
const _SEGS_={ //不放在data中是为了避免不必要的双向绑定
  customer:[
    {t:'s',n:"name"},
    {t:'s',n:"taxid"},
    {t:'s',n:"address"},
    {t:'s',n:"business"},
    {t:'s',n:"creator"},
    {t:'d',n:"createAt"}
  ],
  order:[
    {t:'s',n:"cname"},
    {t:'s',n:"taxid"},
    {t:'n',n:"price"},
    {t:'s',n:"creator"},
    {t:'d',n:"createAt"}
  ]
};

export default {
inject:['ibf'],
components:{
    "confirm-dialog":ConfirmDialog,
    "alert-dialog":AlertDialog,
    "workflow":Workflow
},
data() {return {
    flowid:this.$route.query.flow,
    did:this.$route.query.did,
    dtlPage:this.$route.query.dtlPage,
    tags:sole_tags,
    alertDlg:null,
    dtl:[],
    flow:{}//流程定义信息{name,maxStep,steps}
}},
created(){
    _WF_.flowDef(this.flowid).then(fd=>{
        this.flow=fd;
        var tags=this.tags[fd.name];
        var segments=_SEGS_[fd.name];
        for(var s of segments) { //初始化标签
            s.s=tags[s.n];
        }
        var defaultVal={cmt:{n:this.tags.cmt,t:'s'}};
        var url="/api/proxy/gettemplate?name="+fd.name;
        this.ibf.template(fd.name, url, defaultVal).then(tmpl=>{
            this.detail(tmpl, segments);
        })
    })
},
mounted(){//不能在created中赋值，更不能在data中
    this.alertDlg=this.$refs.errMsg;
},
methods:{
showDtl() {
    var url=appendParas(this.dtlPage,{id:this.did,flowid:this.flowid,service:this.ibf.SERVICE_CRM});
    this.ibf.goto(url)
},
detail(tmpl, segments) {
    var dtlUrl=appendParas(this.flow.dtlApi,{id:this.did});
    request({method:"GET",url:dtlUrl}, this.ibf.SERVICE_CRM).then(resp=>{
        if(resp.code!=RetCode.OK) {
            if(resp.code==RetCode.NOT_EXISTS) {
                this.removeWf();
            }
            return;
        }
        var dta=_WF_.formDtlData(resp.data, segments);
        var ext=decodeExt(dta.comment, tmpl);
        if(ext) {
            for(var d of ext) {
                dta.push({k:d.n, v:d.v});
            }
        }
        this.dtl=dta;
    })
},
removeWf() { //数据不存在，工作流数据错乱的情况下，删除工作流记录
    this.$refs.confirmDlg.show(this.tags.wrongFlowState, ()=>{
        _WF_.remove(this.flowid,this.did, this.ibf.SERVICE_CRM).then(resp=>{
            if(resp.code!=RetCode.OK) {
                this.$refs.errMsg.showErr(resp.code, resp.info);
            }else{
                this.ibf.back();
            }
        })
    })
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat round icon="arrow_back" dense @click="ibf.back"></q-btn>
    <q-toolbar-title>{{flow.dispName}}</q-toolbar-title>
    <q-btn flat :icon="tags.icons[flow.name]" @click="showDtl" v-if="dtlPage"></q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-sm">
<q-list dense>
  <q-item v-for="d in dtl" dense>
    <q-item-section>{{d.k}}</q-item-section>
    <q-item-section>{{d.v}}</q-item-section>
  </q-item>
</q-list>
<q-separator color="primary" inset></q-separator>
<workflow :service="ibf.SERVICE_CRM" :flowid="flowid" :did="did"
 :flowTags="tags.flowTags" :alertDlg="alertDlg"></workflow>
    </q-page>
  </q-page-container>
</q-layout>
<alert-dialog :title="tags.alert" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
<confirm-dialog :title="tags.alert" :close="tags.cancel" :ok="tags.ok" ref="confirmDlg"></confirm-dialog>
`
}